import { common } from '@kit.AbilityKit';
import { HealthKitManager, WorkoutSummary } from '../logic/HealthKitManager';
import { DataExporter } from '../logic/DataExporter';
import { promptAction } from '@kit.ArkUI';

@Entry
@Component
struct Index {
  @State message: string = '华为运动数据同步工具';
  @State isAuthorized: boolean = false;
  @State workouts: WorkoutSummary[] = [];
  @State isLoading: boolean = false;

  private healthManager?: HealthKitManager;
  private dataExporter?: DataExporter;

  aboutToAppear() {
    const context = getContext(this) as common.UIAbilityContext;
    this.healthManager = HealthKitManager.getInstance(context);
    this.dataExporter = new DataExporter(context);
  }

  async handleAuthorize() {
    if (this.healthManager) {
      this.isLoading = true;
      const result = await this.healthManager.requestPermissions();
      this.isAuthorized = (result === "SUCCESS");
      this.message = result === "SUCCESS" ? "授权成功" : result;
      this.isLoading = false;
    }
  }

  async handleFetchData() {
    if (this.healthManager) {
      this.isLoading = true;
      this.workouts = await this.healthManager.fetchAllWorkouts();
      this.message = `同步到 ${this.workouts.length} 条记录`;
      this.isLoading = false;
    }
  }

  async handleExport() {
    if (this.dataExporter && this.workouts.length > 0) {
      this.isLoading = true;
      try {
        const path = await this.dataExporter.exportAllSummaries(this.workouts);
        promptAction.showToast({ message: `导出成功: ${path}` });
        this.message = '导出成功';
      } catch (e) {
        promptAction.showToast({ message: '导出失败' });
      }
      this.isLoading = false;
    } else {
       promptAction.showToast({ message: '请先同步数据' });
    }
  }

  build() {
    Column() {
      Text(this.message)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .margin({ top: 50, bottom: 30 })

      Button('1. 授权健康权限')
        .width('80%')
        .height(50)
        .onClick(() => this.handleAuthorize())
        .enabled(!this.isLoading)
        .margin({ bottom: 20 })

      Button('2. 同步运动记录')
        .width('80%')
        .height(50)
        .onClick(() => this.handleFetchData())
        .enabled(this.isAuthorized && !this.isLoading)
        .margin({ bottom: 20 })

      Button('3. 导出全量数据')
        .width('80%')
        .height(50)
        .onClick(() => this.handleExport())
        .enabled(this.workouts.length > 0 && !this.isLoading)
        .margin({ bottom: 20 })

      if (this.isLoading) {
        LoadingProgress()
          .width(50)
          .height(50)
      }
      
      List({ space: 10 }) {
        ForEach(this.workouts, (item: WorkoutSummary) => {
          ListItem() {
            Column() {
              Text(`类型: ${item.workoutType}`)
              Text(`时间: ${new Date(item.startTime).toLocaleString()}`)
            }.alignItems(HorizontalAlign.Start)
          }
          .padding(10)
          .backgroundColor('#f0f0f0')
          .borderRadius(8)
        })
      }.width('90%').layoutWeight(1).margin({ top: 20 })
    }
    .width('100%')
    .height('100%')
    .padding(20)
  }
}