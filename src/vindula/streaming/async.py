from logging import getLogger

from zope.component import getUtility

from vindula.streaming.utils import getPortal


try:
    from zc.async.interfaces import COMPLETED
except:
    COMPLETED = None

logger = getLogger('vindula.streaming')

QUOTA_NAME = 'vins'

try:
    from plone.app.async.interfaces import IAsyncService
except ImportError:
    pass


def asyncInstalled():
    try:
        import plone.app.async
        return True
    except:
        return False


def isConversion(job, sitepath):
    """
    Check if job is a document viewer conversion job
    """
    from vindula.streaming.eventos import converte_video

    return sitepath == job.args[1] and job.args[4] == converte_video


class JobRunner(object):
    """
    helper class to setup the quota and check the
    queue before adding it to the queue
    """

    def __init__(self, object):
        self.object = object
        self.objectpath = self.object.getPhysicalPath()
        self.portal = getPortal(object)
        self.portalpath = self.portal.getPhysicalPath()
        self.async = getUtility(IAsyncService)
        self.queue = self.async.getQueues()['']

    def is_current_active(self, job):
        return isConversion(job, self.portalpath) and \
            job.args[0] == self.objectpath and \
            job.status != COMPLETED

    @property
    def already_in_queue(self):
        """
        Check if object in queue
        """
        return self.find_job()[0] > -1

    def find_position(self):
        # active in queue
        try:
            return self.find_job()[0]
        except KeyError:
            return -1

    def find_job(self):
        # active in queue
        if QUOTA_NAME not in self.queue.quotas:
            return -1, None
        for job in self.queue.quotas[QUOTA_NAME]._data:
            if self.is_current_active(job):
                return 0, job

        jobs = [job for job in self.queue]
        for idx, job in enumerate(jobs):
            if self.is_current_active(job):
                return idx + 1, job
        return -1, None

    def set_quota(self):
        """
        Set quota for document viewer jobs
        """
        #TODO: Ver isso!

        # registry = getUtility(IRegistry)
        # settings = registry.forInterface(IStreamingSettings)
        # size = settings.async_quota_size

        size = 2
        if QUOTA_NAME in self.queue.quotas:
            if self.queue.quotas[QUOTA_NAME].size != size:
                self.queue.quotas[QUOTA_NAME].size = size
                logger.info("quota %r configured in queue %r", QUOTA_NAME,
                            self.queue.name)
        else:
            self.queue.quotas.create(QUOTA_NAME, size=size)
            logger.info("quota %r added to queue %r", QUOTA_NAME,
                        self.queue.name)

    def queue_it(self):
        from vindula.streaming.eventos import converte_video

        self.async.queueJobInQueue(self.queue, (QUOTA_NAME,), converte_video,
                                   self.object)
        #TODO: Ver isso!

        # settings = StreamingSettingsEditForm(self.object)
        # settings.converting = True

    def move_to_front(self):
        """
        Queue data is stored in buckets of queues.
        Because of this, you need to go through each
        bucket and find where the actual job is,
        then move it to the first bucket, first item
        of queue.
        """
        position, job = self.find_job()
        if position <= 1:
            return
        found_bucket = None
        for bucket in self.queue._queue._data:
            if job in bucket._data:
                found_bucket = bucket
                break
        jobs = list(found_bucket._data)
        jobs.remove(job)
        found_bucket._data = tuple(jobs)

        bucket = self.queue._queue._data[0]
        jobs = list(bucket._data)
        jobs.insert(0, job)
        bucket._data = tuple(jobs)


def queueJob(object):
    """
    queue a job async if available.
    otherwise, just run normal
    """
    from vindula.streaming.eventos import converte_video
    
    if asyncInstalled():
        try:
            runner = JobRunner(object)
            runner.set_quota()
            if runner.already_in_queue:
                logger.info('object %s already in queue for conversion' % (
                    repr(object)))
            else:
                runner.queue_it()
            return
        except:
            logger.exception("Error using plone.app.async with "
                "collective.documentviewer. Converting pdf without "
                "plone.app.async...")
            converte_video()
    else:
        converte_video()
