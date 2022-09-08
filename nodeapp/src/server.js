import express from 'express';
import cors from 'cors'
import { sequelize } from './sequelize.js';

import { IndexRouter } from './controllers/v0/index.router.js';
import { config } from './config/config.js';
import bodyParser from 'body-parser';

import { v0models } from './controllers/v0/model.index.js';


sequelize.authenticate().then(() => {
   console.log('Connection has been established successfully.');
}).catch((error) => {
   console.error('Unable to connect to the database: ', error);
});

// sequelize.sync().then(() => {
//    console.log('Book table created successfully!');
// }).catch((error) => {
//    console.error('Unable to create table : ', error);
// });

(async () => {

  const app = express();
  const port = process.env.PORT || 8080; // default port to listen
  
  app.use(cors());
  app.use(bodyParser.json());

  //CORS Should be restricted
  app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "http://localhost:8100");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization");
    next();
  });

  app.use('/api/v0/', IndexRouter)

  // Root URI call
  app.get( "/", async ( req, res ) => {
    res.send( "welcome to the root of this API" );
  } );
  

  // Start the Server
  app.listen( port, () => {
      console.log( `server running http://localhost:${ port }` );
      console.log( `press CTRL+C to stop server` );
  } );
})();
