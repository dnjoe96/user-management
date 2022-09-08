import { Sequelize } from 'sequelize';
import { config } from './config/config.js';


export const sequelize = new Sequelize(
  config.dev.database,
  config.dev.username,
  config.dev.password,
  {
    host: config.dev.host,
    dialect: config.dev.dialect
  }
);
