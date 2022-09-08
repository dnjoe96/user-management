import { Router } from 'express';
// import { FeedRouter } from './feed/routes/feed.router.js';
import { UserRouter } from './users/routes/user.router.js';

const router = Router();

// router.use('/feed', FeedRouter);
router.use('/user', UserRouter);

router.get('/', async (req, res) => {    
    res.send(`V0`);
});

export const IndexRouter = router;
