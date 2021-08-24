import {
  Controller,
  Get,
  Param,
  Patch,
  Post,
  Put,
  Query,
} from "@nestjs/common";
import { ApiOkResponse, ApiParam, ApiQuery, ApiTags } from "@nestjs/swagger";
import { VoucherService } from "../services/voucher.service";

@Controller("voucher")
@ApiTags("查询")
export class VoucherController {
  constructor(private voucherService: VoucherService) {}
  @Get("/findAll")
  async findAll() {
    return this.voucherService.findInfoByDescribe("");
  }

  @Get("/findInfoByCity/:city")
  @ApiParam({ name: "city", description: "city:城市中文名" })
  async findInfoByCity(@Param("city") city: string) {
    console.log(city);
    return this.voucherService.findInfoByCity(city);
  }
  @Get("/findInfoByProvince/:province")
  @ApiParam({ name: "province", description: "province:省份中文名" })
  async findInfoByProvince(@Param("province") province: string) {
    console.log(province);
    return this.voucherService.findInfoByProvince(province);
  }
  @Get("/findInfoByDescribe")
  @ApiParam({ name: "des", description: "des:描述信息模糊关键字" })
  async findInfoByDescribe(@Query("des") des: string) {
    return this.voucherService.findInfoByDescribe(des);
  }

  @Get("/findInfoByGiveMethod")
  @ApiQuery({
    name: "method",
    description: "method:领取方式（领取/抢券/摇号）",
  })
  async findInfoByGiveMethod(@Query("method") method: string) {
    return this.voucherService.findInfoByGiveMethod(method);
  }

  @Get("/flashData")
  async flashData() {
    return this.voucherService.flashData();
  }
}
