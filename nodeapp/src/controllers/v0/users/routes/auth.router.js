// import { Session } from '@sentry/node';
import * as bcrypt from 'bcrypt';
import * as jwt from 'jsonwebtoken';

import { config } from '../../../../config/config.js';
import { User } from '../models/Userc.js';
import { Session } from '../models/Session.js';

export async function generatePassword(plainTextPassword) {
  //@TODO Use Bcrypt to Generated Salted Hashed Passwords
  const salt = await bcrypt.genSalt(10);
  // now we set user password to hashed password
  const password = await bcrypt.hash(plainTextPassword, salt);
  return password
}

export async function comparePasswords(plainTextPassword, hash) {
  //@TODO Use Bcrypt to Compare your password to your Salted Hashed Password
  const validPassword = await bcrypt.compare(plainTextPassword, hash);
  if (validPassword) {
    return true
  } else {
    return false
  }
}

export function generateJWT(user) {
  //@TODO Use jwt to create a new JWT Payload containing
  return jwt.sign(user.toJSON(), config.jwt.secret);
}

export async function requireAuth(req, res, next) {
  if (!req.headers || !req.headers.authentication){
      return res.status(401).send({ message: 'No authentication headers.' });
  }
  
  const sessionid = req.headers.authentication;

  let session;
  try {
    session = await Session.findOne({ where: {token: sessionid}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }

  if(!session) {
      res.status(401).send({status: 'false', message: 'Login required'});
  }

  let user;
  try {
    user = await User.findOne({ where: {id: session.user_id}});
  } catch (err) {
    res.status(400).send({status: "false", message: `${err}`});
  }
  
  res.current_user = user;  
  return next();
}
