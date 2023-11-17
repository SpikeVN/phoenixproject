import random

import configuration as cfg
import gcloud_helper
import logutils
import phoenix


def update_commands(bot: phoenix.Bot):
    result = (
        gcloud_helper.sheets_service.spreadsheets()
        .values()
        .get(spreadsheetId=cfg.get("backend.configSheet"), range="13:32")
        .execute()
    ).get("values", [])
    for row in result:
        if len(row) > 1:

            def ccb(r: list[str]):
                nrow = row.copy()

                def cb(ctx: phoenix.Context, args: list[str]) -> bool:
                    if len(nrow) == 2:
                        ctx.reply(
                            "xác định lệnh lỗi: k định nghĩa câu trl. W bot, L human"
                        )
                        return True
                    if len(args) != 0:
                        tok = {}
                        for i, t in enumerate(nrow[1].split()[1:]):
                            if t[0] == "%" and t[-1] == "%":
                                if t[1] == "*":
                                    tok[t[2:-1]] = args
                                else:
                                    tok[t[1:-1]] = args[i]
                        response = random.choice(nrow[2:])
                        if len(tok) != len(args):
                            ctx.reply(
                                "số tham số trong template không trùng với tham số mà mày đút vào. you L bruh"
                            )
                            return True
                        for k, v in tok.items():
                            if isinstance(v, list):
                                response = response.replace(f"%*{k}%", " ".join(v))
                            else:
                                response = response.replace(f"%{k}%", v)
                        ctx.reply(response.replace("\\n", "\n"))
                    else:
                        ctx.reply(random.choice(nrow[2:]).replace("\\n", "\n"))
                    return True

                return cb

            try:
                bot.add_or_edit_command(row[1].split()[0], ccb(row))
            except IndexError:
                logutils.error("Invalid syntax found. Ignoring and moving on.")
                pass


class ShitpostUpdater(phoenix.Module):
    @phoenix.cmd_def(name="refresh")
    def refresh(self, ctx: phoenix.Context, args: list[str]) -> bool:
        update_commands(self.bot)
        ctx.reply("update thanh cong!")
        return True


def get(bot: phoenix.Bot):
    update_commands(bot)
    return ShitpostUpdater(bot)
