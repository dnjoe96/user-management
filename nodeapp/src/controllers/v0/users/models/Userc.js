import { DataTypes } from "sequelize";
import { sequelize } from "../../../../sequelize.js";

export const User = sequelize.define("User", {
   id: {
     type: DataTypes.STRING,
     allowNull: false,
     primaryKey: true
   },
   username: {
     type: DataTypes.STRING,
     allowNull: false,
     unique: true
   },
   firstname: {
     type: DataTypes.STRING,
     allowNull: false
   },
   lastname: {
     type: DataTypes.STRING,
     allowNull: false
   },
   middlename: {
     type: DataTypes.STRING,
     allowNull: true
   },
   email: {
     type: DataTypes.STRING,
     allowNull: false,
     unique: true
   },
   phone: {
     type: DataTypes.STRING,
     allowNull: true
   },
   city: {
     type: DataTypes.STRING,
     allowNull: true
   },
   state: {
     type: DataTypes.STRING,
     allowNull: true
   },
   country: {
     type: DataTypes.STRING,
     allowNull: true
   },
   group: {
     type: DataTypes.STRING,
     allowNull: true
   },
   active: {
     type: DataTypes.STRING,
     allowNull: false,
     defaultValue: 0
   },
   rank: {
     type: DataTypes.STRING,
     allowNull: true
   },
   date_created: {
     type: DataTypes.DATE,
     allowNull: false,
     defaultValue: DataTypes.NOW
   },
   date_updated: {
     type: DataTypes.DATE,
     allowNull: true
   },
   activation_token: {
     type: DataTypes.INTEGER,
     allowNull: true
   },
   deletion_flag: {
     type: DataTypes.STRING,
     allowNull: true
   }
}, {
  tableName: 'user', // insisting the table name i want
  // timestamps: false,
  createdAt: false, // If don't want createdAt
  updatedAt: false // If don't want updatedAt
});