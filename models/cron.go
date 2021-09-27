package models

import (
	"math/rand"
	"strconv"

	"github.com/beego/beego/v2/adapter/logs"
	"github.com/robfig/cron/v3"
)

var c *cron.Cron

func initCron() {
	c = cron.New()
	if Config.DailyAssetPushCron != "" {
		_, err := c.AddFunc(Config.DailyAssetPushCron, DailyAssetsPush)
		if err != nil {
			logs.Warn("资产推送任务失败：%v", err)
		} else {
			logs.Info("资产推送任务就绪")
		}
		c.AddFunc("3 */1 * * *", initVersion)
		c.AddFunc("40 */1 * * *", GitPullAll)
		//12小时cookie过期禁用检测 需要配置Ctime 随机分钟数
		c.AddFunc("0 "+strconv.Itoa(rand.Intn(59))+" "+Config.CTime+"/12 * * ?", initCookie)

	}
	c.Start()
}
