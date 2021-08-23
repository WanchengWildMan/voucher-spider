import { Column, Entity, PrimaryColumn, PrimaryGeneratedColumn } from "typeorm";
@Entity()
export class Voucher {
  @PrimaryColumn({ nullable: false, unique: true })
  city: string;
  @Column("varchar",{nullable:true,unique:false})
  province:string;
  @Column("double", { nullable: true })
  gdp19: number;
  @Column("double", { nullable: true })
  gdpStage19: string;
  @Column("double", { nullable: true })
  peo: number;
  @Column("double")
  lon: number;
  @Column("double")
  lat: number;
  @Column("double", { nullable: true })
  moneyDigit: number;

  @Column("varchar")
  giveOutMethod: string;
  @Column("varchar")
  methodDescribe: string;
  @Column("varchar")
  giveTimeDescribe;
  @Column("varchar")
  moneyDescribe: string;
  @Column("varchar")
  numDescribe: string;
  @Column("varchar")
  ruleDescribe: string;
  @Column("varchar")
  url: string;
  //        'lat'
  //        {"2019年gdp": "gdp19", "城市经济分级_2019年gdp": "gdp_stage19", "人口": "peo", "发放方式0领取1摇号2抢券": "give_out_method",
  //                                 "领取方式": "method_describe", "发放时间": "give_time_describe", "发放金额": "money_describe", "领取数量": "num_describe", "领取规则": "rule_describe", "链接": "url"}
}
