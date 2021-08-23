import { Module } from "@nestjs/common";
import { TypeOrmModule } from "@nestjs/typeorm";
import { Voucher } from "src/entities/voucher.entity";
import { AppController } from "./app.controller";
import { AppService } from "./app.service";
import { VoucherController } from "./controllers/voucher.controller";
import { VoucherService } from "./services/voucher.service";
const entities = [Voucher];
@Module({
  imports: [
    //module在这里导入
    TypeOrmModule.forRootAsync({
      useFactory: () => ({
        type: "mysql",
        host: "localhost",
        port: 3306,
        username: "test",
        password: "test",
        database: "test",
        synchronize: true,
        logging: true,
        entities: entities,
        migrations: ["../migration/**/*.ts"],
        subscribers: ["../subscriber/**/*.ts"],
      }),
    }),
    TypeOrmModule.forRoot(),
    TypeOrmModule.forFeature(entities),

  ],
  controllers: [AppController,VoucherController],
  providers: [AppService,VoucherService],
})
export class AppModule {}
