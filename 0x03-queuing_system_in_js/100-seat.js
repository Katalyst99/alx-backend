import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

const app = express();
const client = createClient();
const queue = createQueue();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

const INITIAL_SEATS = 50;
let reservationEnabled = true;

async function reserveSeat(seats) {
  await setAsync('available_seats', seats);
};

async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats !== null ? parseInt(seats, 10) : null;
};
reserveSeat(INITIAL_SEATS);

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat').save((err) => {
    if (err) {
      return res.json({ status: 'Reservation failed' });
    }
    res.json({ status: 'Reservation in process' });
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    const seats = await getCurrentAvailableSeats();

    if (seats <= 0) {
      reservationEnabled = false;
      return done(new Error('Not enough seats available'));
    }

    await reserveSeat(seats - 1);

    if (seats - 1 === 0) {
      reservationEnabled = false;
    }

    done();
  });
});

const PORT = 1245;
app.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
