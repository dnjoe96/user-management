import { compare, hash } from 'bcrypt';
import { DataTypes, Model } from 'sequelize';

import { tokenHelper, mailHelper } from '@/helpers';

export default function (sequelize) {
  class User extends Model {
    get fullName() {
      return `${this.firstname} ${this.lastname}`;
    }

    generateToken(expiresIn = '1h') {
      const data = { id: this.id, email: this.email };
      return tokenHelper.generateToken(data, expiresIn);
    }

    // validatePassword(plainPassword) {
    //   return compare(plainPassword, this.password);
    // }

    // sendMail(mail) {
    //   const payload = { ...mail, to: `${this.fullName} <${this.email}>` };
    //   return mailHelper.sendMail(payload);
    // }

    static associate(models) {
      User.hasMany(models.tweet, { foreignKey: 'userId' });
    }
  }

  User.init({
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
     allowNull: no,
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
     type: DataTypes.DATEO,
     allowNull: true
   },
   activation_token: {
     type: DataTypes.INTEGER,
     allowNull: true
   },
   deletion_flag: {
     type: DataTypes.STRING,
     allowNull: true
   },
  }, {
    modelName: 'user',
    sequelize,
  });

  User.addHook('beforeSave', async (instance) => {
    if (instance.changed('password')) {
      // eslint-disable-next-line no-param-reassign
      instance.password = await hash(instance.password, 10);
    }
  });

  User.addHook('afterCreate', (instance) => {
    // Send welcome message to user.
    const payload = {
      subject: 'Welcome to Express Starter',
      html: 'Your account is created successfully!',
    };
    instance.sendMail(payload);
  });

  User.addHook('afterDestroy', (instance) => {
    // Send good by message to user.
    const payload = {
      subject: 'Sorry to see you go',
      html: 'Your account is destroyed successfully!',
    };
    instance.sendMail(payload);
  });

  return User;
}