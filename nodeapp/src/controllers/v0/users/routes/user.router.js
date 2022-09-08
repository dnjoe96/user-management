import { Router } from 'express';

// import { User } from '../models/User.js';
// import { AuthRouter, requireAuth } from './auth.router.js';

const router = Router();

// router.use('/user', AuthRouter);

router.get('/', async (req, res) => {
  res.status(200).send('I work')
});

router.get('/:id', async (req, res) => {
    let { id } = req.params;
    const item = await User.findByPk(id);
    res.send(item);
});

export const UserRouter = router;