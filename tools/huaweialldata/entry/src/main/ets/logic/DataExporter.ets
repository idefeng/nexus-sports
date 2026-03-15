import { fileIo as fs } from '@kit.CoreFileKit';
import { common } from '@kit.AbilityKit';
import { hilog } from '@kit.PerformanceAnalysisKit';

const TAG = 'DataExporter';

export class DataExporter {
  private context: common.UIAbilityContext;

  constructor(context: common.UIAbilityContext) {
    this.context = context;
  }

  /**
   * 将数据导出为 JSON 文件并保存到沙盒目录
   */
  public async exportToJson(data: Object, fileName: string): Promise<string> {
    const jsonString = JSON.stringify(data, null, 2);
    const filePath = `${this.context.filesDir}/${fileName}.json`;

    try {
      let file = await fs.open(filePath, fs.OpenMode.READ_WRITE | fs.OpenMode.CREATE | fs.OpenMode.TRUNC);
      await fs.write(file.fd, jsonString);
      await fs.close(file);
      hilog.info(0x0000, TAG, 'exportToJson success: %{public}s', filePath);
      return filePath;
    } catch (error) {
      hilog.error(0x0000, TAG, 'exportToJson failed: %{public}s', JSON.stringify(error));
      throw new Error(`Export failed: ${JSON.stringify(error)}`);
    }
  }

  /**
   * 模拟导出所有运动记录摘要
   */
  public async exportAllSummaries(workouts: Object[]): Promise<string> {
    return await this.exportToJson(workouts, `huawei_workouts_${Date.now()}`);
  }
}
