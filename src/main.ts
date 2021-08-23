import { NestFactory } from "@nestjs/core";
import { AppModule } from "./app.module";

import { SwaggerModule, DocumentBuilder } from "@nestjs/swagger";
var exec = require("child_process").exec;
async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  // 为了创建完整的文档（具有定义的HTTP路由），我们使用类的createDocument()方法SwaggerModule。此方法带有两个参数，分别是应用程序实例和基本Swagger选项。
  const options = new DocumentBuilder()
    .setTitle("消费券")
    .setDescription("使用nest书写的常用性接口") // 文档介绍
    .setVersion("1.0.0") // 文档版本

    .addTag("查询")
    .setBasePath("http://localhost:30000")
    .build();
  const document = SwaggerModule.createDocument(app, options);
  // 最后一步是setup()。它依次接受（1）装入Swagger的路径，（2）应用程序实例, （3）描述Nest应用程序的文档。

  SwaggerModule.setup("/apiDocument", app, document);

  // exec(SPIDER_COMMAND, function (error, stdout, stderr) {
  //   if (error) {
  //     console.error("stderr : " + stderr);
  //   }
  //   console.log("exec: " + stdout);
  // });
  await app.listen(30000);
}
bootstrap();
export const SPIDER_COMMAND = "python3 -u quan_spider.py";
