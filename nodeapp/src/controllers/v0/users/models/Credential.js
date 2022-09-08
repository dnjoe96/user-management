import { DataTypes } from "sequelize";
import { sequelize } from "../../../../sequelize.js";

export const Credential = sequelize.define("credentials", {
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
   password: {
     type: DataTypes.STRING,
     allowNull: false
   },
   date_updated: {
     type: DataTypes.DATE,
     allowNull: true
   },
}, {
  tableName: 'credentials', // insisting the table name i want
  // timestamps: false,
  createdAt: false, // If don't want createdAt
  updatedAt: false // If don't want updatedAt
});
