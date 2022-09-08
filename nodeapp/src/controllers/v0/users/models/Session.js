import { DataTypes } from "sequelize";
import { sequelize } from "../../../../sequelize.js";

export const Session = sequelize.define("sessions", {
   id: {
     type: DataTypes.INTEGER,
     allowNull: false,
     autoIncrement: true,
     unique: true,
     primaryKey: true
   },
   user_id: {
     type: DataTypes.STRING,
     allowNull: false,
    //  references: {
    //     model: 'user', // table name
    //     key: 'id' // the key being referenced
    //  }
   },
   token: {
     type: DataTypes.STRING,
     allowNull: false
   },
   date_created: {
     type: DataTypes.DATE,
     allowNull: true
   },
}, {
  tableName: 'sessions', // insisting the table name i want
  // timestamps: false,
  createdAt: false, // If don't want createdAt
  updatedAt: false // If don't want updatedAt
});
