import { expect } from 'chai';
import kue from 'kue';
import createPushNotificationsJobs from './8-job.js';

describe('createPushNotificationsJobs', () => {
  let queue;
  beforeEach(() => {
    queue = kue.createQueue();
    queue.testMode.enter();
  });

  afterEach(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it('should display an error message if jobs is not an array', () => {
    expect(() => createPushNotificationsJobs(42, queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs('invalid', queue)).to.throw('Jobs is not an array');
    expect(() => createPushNotificationsJobs({}, queue)).to.throw('Jobs is not an array');
  });

  it('should create two new jobs in the queue', () => {
    const jobs = [
      { phoneNumber: '4153518780', message: 'Code 1234' },
      { phoneNumber: '4153518781', message: 'Code 5678' },
    ];

    createPushNotificationsJobs(jobs, queue);

    expect(queue.testMode.jobs.length).to.equal(2);

    const [job1, job2] = queue.testMode.jobs;
    expect(job1.type).to.equal('push_notification_code_3');
    expect(job1.data).to.deep.equal({ phoneNumber: '4153518780', message: 'Code 1234' });
    expect(job2.type).to.equal('push_notification_code_3');
    expect(job2.data).to.deep.equal({ phoneNumber: '4153518781', message: 'Code 5678' });
  });
});

