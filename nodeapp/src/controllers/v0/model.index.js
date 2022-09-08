// import { FeedItem } from './feed/models/FeedItem.js';
import { User } from './users/models/Userc.js';
import { Session } from './users/models/Session.js';
import { Credential } from './users/models/Credential.js';

// Credential.hasMany(User);
// Session.hasMany(User);
export const v0models = [ Credential, Session, User ];
