import {Table, Column, Model, HasMany, PrimaryKey, CreatedAt, UpdatedAt, ForeignKey} from 'sequelize';
import { User } from '../../users/models/User';

// @Table
// export class FeedItem extends Model<FeedItem> {
//   @Column
//   public caption!: string;

//   @Column
//   public url!: string;

//   @Column
//   @CreatedAt
//   public createdAt: Date = new Date();

//   @Column
//   @UpdatedAt
//   public updatedAt: Date = new Date();
// }
