import datetime
import phoenix
import configuration as cfg
import gcloud


class Reminder(phoenix.Module):
    def __init__(self, bot):
        super().__init__(bot)
        self.events = None
        self.invalidation = datetime.datetime.now()

    def update_events(self):
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        events_result = (
            gcloud.calendar_service.events()
            .list(
                calendarId=cfg.get("modules.gcal.calid"),
                timeMin=now,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        self.events = events_result.get("items", [])

        if not self.events:
            self.events = []

    @phoenix.cmd_def(name="wuc")
    def whatsup_chitiet(self, ctx: phoenix.Context, args: list[str]) -> bool:
        if (
            self.events is None
            or datetime.datetime.now() - self.invalidation
            > datetime.timedelta(minutes=1)
        ):
            self.update_events()
        try:
            e = self.events[int(args[0]) - 1]
            ctx.reply(
                f"thông tin chi tiết:\ntên: {e.get('summary', 'không có')}\ntạo bởi: {e.get('creator', {'email': 'không có'}).get('email')}\nmô tả: {e.get('description', 'không có')}"
            )
        except IndexError:
            ctx.reply(f"stt không tồn tại, check lại não khỉ của m đi")
        return True

    @phoenix.cmd_def(name="wu")
    def whatsup(self, ctx: phoenix.Context, args: list[str]) -> bool:
        # Call the Calendar API
        ctx.reply("đang lập báo cáo...")
        if (
            self.events is None
            or datetime.datetime.now() - self.invalidation
            > datetime.timedelta(minutes=1)
        ):
            self.update_events()
        ev_str = []
        for i, event in enumerate(self.events):
            start = datetime.datetime.fromisoformat(
                event["start"].get("dateTime", event["start"].get("date"))
            ) - datetime.datetime.now(
                tz=datetime.timezone(datetime.timedelta(hours=-7))
            )
            ev_str.append(
                f"{i+1}. Sau {f'{start.days} ngày ' if start.days != 0 else ''}{start.seconds/60/60:.0f}h nữa: {event['summary']}"
            )
        if len(ev_str) == 0:
            ctx.reply(
                "ok xong r: không có công việc nào trong thời gian tới đã được đặt."
            )
        ctx.reply(
            "ok xong r\n" + "\n".join(ev_str) + "\nchi tiết hơn nhập `!wuc <STT>`."
        )
        return True


def get(bot: phoenix.Bot) -> phoenix.Module:
    return Reminder(bot)
