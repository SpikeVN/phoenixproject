import phoenix


class General(phoenix.Module):
    @phoenix.cmd_def(name="help")
    def help(self, ctx: phoenix.Context, args: list[str]) -> bool:
        ctx.reply(
            "trợ giúp:\n"
            + "\n".join(f"!{cmdname}" for cmdname in phoenix.COMMAND_REGISTRY.keys())
            + "\n"
            + "\n".join(f"!{cmdname}" for cmdname in self.bot.botcmds.keys())
            + "\n\nMessage from saul goodman: This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more details.\nhttps://github.com/SpikeVN/phoenixproject"
        )
        return True

    @phoenix.cmd_def(name="tth")
    def tth(self, ctx: phoenix.Context, args: list[str]) -> bool:
        ctx.reply("m phản động ít th")
        return True


def get(bot: phoenix.Bot) -> phoenix.Module:
    return General(bot)
