import phoenix


class General(phoenix.Module):
    @phoenix.cmd_def(name="help")
    def help(self, ctx: phoenix.Context, args: list[str]) -> bool:
        ctx.reply(
            "trợ giúp:\n"
            + " ".join(f"!{cmdname}" for cmdname in phoenix.COMMAND_REGISTRY.keys())
            + "\n"
            + " ".join(f"!{cmdname}" for cmdname in self.bot.botcmds.keys())
        )
        return True

    @phoenix.cmd_def(name="shutdown")
    def shutdown(self, ctx: phoenix.Context, args: list[str]):
        exit(0)

    @phoenix.cmd_def(name="tth")
    def tth(self, ctx: phoenix.Context, args: list[str]) -> bool:
        ctx.reply("m phản động ít th")
        return True


def get(bot: phoenix.Bot) -> phoenix.Module:
    return General(bot)
