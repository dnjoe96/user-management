import * as bcrypt from 'bcrypt';
import * as jwt from 'jsonwebtoken';

import { config } from '../../../../config/config.js';


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

export function requireAuth(req, res, next) {
    console.warn("auth.router not yet implemented, you'll cover this in lesson 5")
    return next();
    // if (!req.headers || !req.headers.authorization){
    //     return res.status(401).send({ message: 'No authorization headers.' });
    // }
    

    // const token_bearer = req.headers.authorization.split(' ');
    // if(token_bearer.length != 2){
    //     return res.status(401).send({ message: 'Malformed token.' });
    // }
    
    // const token = token_bearer[1];

    // return jwt.verify(token, "hello", (err, decoded) => {
    //   if (err) {
    //     return res.status(500).send({ auth: false, message: 'Failed to authenticate.' });
    //   }
    //   return next();
    // });
}
