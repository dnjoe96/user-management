import { Router } from 'express';
import { v4 as uuidv4 } from 'uuid';
import { User } from '../models/Userc.js';
import { Credential } from '../models/Credential.js';
import { Session } from '../models/Session.js';
import { requireAuth, generatePassword, comparePasswords } from './auth.router.js';

const router = Router();

router.get('/', async (req, res) => {
  // user index view
  res.status(200).send('This the node js api root for user mgt. I work')
});

router.post('/login', async (req, res) => {
  const username = req.body.username;
  const password = req.body.password;
  // check email is valid
  // if (!email || !EmailValidator.validate(email)) {
  //     return res.status(400).send({ auth: false, message: 'Email is required or malformed' });
  // }

  // check email password valid
  if (!password) {
      return res.status(400).send({ auth: false, message: 'Password is required' });
  }

  let user;
  try {
    user = await User.findOne({ where: {username: username}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  // check that user exists
  if(!user) {
      return res.status(401).send({ auth: false, message: 'Unauthorized' });
  }

  // check that the password matches
  let cred = await Credential.findOne({ where: {user_id: user.id}});

  let password_hash = cred.password;
  const authValid = await comparePasswords(password, password_hash)

  if(!authValid) {
    res.status(401).send({ auth: false, message: 'Unauthorized' });
  }

  try {
    let session = await Session.findOne({ where: {user_id: user.id}});
    if(session) {
      res.status(401).send({status: 'false', message: 'you are already logged in', session_id: session.token});
    }
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }

  
  const sessionid = uuidv4();
// console.log(data);

  const session = await new Session({
    user_id: user.id,
    token: sessionid,
    data_created: new Date().getDate()
  })

  let savedSession;
  try {
      savedSession = await session.save();
  } catch (e) {
      console.log(e);
  }

  res.status(200).send({
    'status': 'true',
    'message': `${user.username} logged in successfully`,
    'session_id': sessionid
  });
});


router.delete('/logout', requireAuth, async (req, res) => {
  // logout endpoint

  let session;
  try {
    session = await Session.findOne({ where: {token: req.headers.authentication}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  console.log('got here');
  if (session) {
    session.destroy();
    res.removeHeader('current_user');
    res.status(200).send({status: true, message: 'you are logged out, bye'});
  }
  res.status(400).send({status: true, message: 'You are not logged in'});
});


router.post('/register', async (req, res) => {
  // user register endpoint
  const data = req.body
  const compulsory = ['username', 'firstname', 'lastname', 'email', 'password']
  
  if (!data.password || !data.username || !data.firstname || !data.lastname || !data.email) {
      return res.status(400).send({ status: false, message: 'compulsory fields are username, password, email, firstname, lastname' });
  }

  // find the user
  let user;
  try {
    user = await User.findOne({where: {email: data.email}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  // check that user doesnt exists
  if(user) {
      return res.status(422).send({ auth: false, message: 'User may already exist' });
  }

  const password_hash = await generatePassword(data.password);

  delete data.password;
  data.id = uuidv4();
  data.activation_token = Math.floor(Math.random() * 10001).toString();
  // console.log(data);
  
  const newUser = await new User(data);
  const cred = await new Credential({
    user_id: data.id,
    date_updated: new Date().getDate(),
    password: password_hash
  })

  let savedCred;
  let savedUser;
  try {
      savedUser = await newUser.save();
      savedCred = await cred.save();
  } catch (e) {
      console.log(e);
  }
  // console.log(savedCred, savedUser);
  // // Generate JWT
  // const jwt = generateJWT(savedUser);

  res.status(200).send({
    status: 'true',
    message: `User ${data.username} has been created`,
    user_id: data.id,
    activation_token: data.activation_token
  })
});

router.get('/profile/:username', requireAuth, async (req, res) => {
  // user profile endpoint
  const data = req.params

  if ( res.current_user.username !== data.username ) {
    res.status(401).send({status: 'false', message: 'You need to login, to access resourse'})
  }
  res.status(200).send({status: 'true', user: res.current_user})
});

router.put('/edit/:username', async (req, res) => {
  // user edit endpoint
  const username = req.params.username
  const data = req.body

  let user;
  try {
    user = await User.findOne({where: {username: username}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  // check that user exists
  if(!user) {
      return res.status(400).send({ status: 'false', message: 'User not found' });
  }

  for ( let one in data ) {
    if (one === 'username' || one === 'password') {
      return res.status(400).send({ status: 'false', message: `${one} is not a valid field`});
    }
  }

  
  try {
    user.update(data);
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  res.status(200).send({'status': 'true', 'message': 'record updated'})
});


router.get('/activate/:user_id/:token', async (req, res) => {
  // user account activation endpoint
  const data = req.params
  console.log(data);

  if (!data.user_id || !data.token) {
    res.status(400).send({status: 'false', message: 'invalid token'});
  }

  let user;
  try {
    user = await User.findOne({ where: {id: data.user_id}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  // check that user doesnt exists
  if(!user) {
      res.status(401).send({status: 'false', message: 'invalid user'});
  } else if (user.active === '1') {
      res.status(400).send({status: "false", message: `User ${user.username} already activated`});
  } else if (user.activation_token !== data.token) {
      res.status(200).send({status: "false", message: `User ${user.username} invalid activation token for user`});
  } else {
    user.update({active: '1', activation_token: ''});
    res.status(200).send({status: 'true', message: `User ${user.username} is activated. Congratulations!!`})
  }
});

router.put('/deactivate', async (req, res) => {
  // account deactivation endpoint

  const data = req.body

  if (!data.username) {
    res.status(400).send({status: 'false', message: 'provide username'})
  }

  let user;
  try {
    user = await User.findOne({where: {username: data.username}});
    if (!user) {
      res.status(404).send({status: "false", message: `user ${data.username} not found`});
    } else {
      user.update()
    }
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  user.update({active: '0'});
  res.status(200).send({status: 'true', message: `User ${user.username} is deactivated`})
});

router.put('/role', async (req, res) => {
  // role assignment endpoint
  res.status(200).send('This is the role assignment endpoint')
});

router.get('/all', async (req, res) => {
  // get all users endpoint
  res.status(200).send('This is the fetch all endpoint')
});

router.get('/verification', 
    // requireAuth, 
    async (req, res) => {
        return res.status(200).send({ auth: true, message: 'Authenticated.' });
});


//register a new user
router.post('/sdsdssdsd', async (req, res) => {
    const email = req.body.email;
    const plainTextPassword = req.body.password;
    // check email is valid
    if (!email || !EmailValidator.validate(email)) {
        return res.status(400).send({ auth: false, message: 'Email is required or malformed' });
    }

    // check email password valid
    if (!plainTextPassword) {
        return res.status(400).send({ auth: false, message: 'Password is required' });
    }

    // find the user
    let user;
    try {
      user = await User.findOne({ where: {id: data.user_id}});
    } catch (err) {
      res.status(400).send({status: "false", message: `${err}`});
    }
    // check that user doesnt exists
    if(user) {
        return res.status(422).send({ auth: false, message: 'User may already exist' });
    }

    const password_hash = await generatePassword(plainTextPassword);

    const newUser = await new User({
        email: email,
        password_hash: password_hash
    });

    let savedUser;
    try {
        savedUser = await newUser.save();
    } catch (e) {
        throw e;
    }

    res.status(201).send({token: jwt, user: savedUser.short()});
});

export const UserRouter = router;
