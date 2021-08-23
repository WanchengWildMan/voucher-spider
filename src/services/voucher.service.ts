import { Injectable } from "@nestjs/common";
import { InjectRepository } from "@nestjs/typeorm";
import { Voucher } from "src/entities/voucher.entity";
import { getConnection, getManager, Repository } from "typeorm";
import { SPIDER_COMMAND } from "../main";
var exec = require("child_process").exec;

@Injectable()
export class VoucherService {
  constructor(
    @InjectRepository(Voucher)
    private readonly $voucherInfo: Repository<Voucher>
  ) {}
  async findInfoByCity(city: string) {
    return await this.$voucherInfo.find({ where: `city LIKE '%${city}'` });
  }
  async findInfoByProvince(province: string) {
    return await this.$voucherInfo.find({
      where: `province LIKE '%${province}'`,
    });
  }
  async findInfoByDescribe(des: string) {
    const connection = getConnection();
    const queryRunner = connection.createQueryRunner();
    await queryRunner.connect();
    return await getManager()
      .createQueryBuilder(Voucher, "v")
      .where(
        `concat(v.methodDescribe,v.giveTimeDescribe,v.moneyDescribe,v.numDescribe,v.ruleDescribe) LIKE '${des}'`
      )
      .getMany();
  }
  /**
   * 根据描述模糊查询
   */
  async findInfoByGiveMethod(giveMethod: string) {
    return await this.$voucherInfo.find({
      giveOutMethod: giveMethod,
    });
  }
  /**
   * 重新爬
   */
  async flashData() {
    exec(SPIDER_COMMAND, function (error, stdout, stderr) {
      if (error) {
        console.error("stderr : " + stderr);
      }
      console.log("exec: " + stdout);
    });
    return "发送刷新请求成功";
  }
}
