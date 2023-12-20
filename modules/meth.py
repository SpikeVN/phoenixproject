import phoenix
from sympy import *
from PIL import Image
import random

x, y, z, t = symbols("x y z t")
k, m, l = symbols("k m l", integer=True)
f, g, h = symbols("f g h", cls=Function)


def pad_img(image, top, right, bottom, left, color):
    width, height = image.size
    new_width = width + right + left
    new_height = height + top + bottom
    result = Image.new(image.mode, (new_width, new_height), color)
    result.paste(image, (left, top))
    return result


def preproc_input(args: list[str]) -> str:
    if ("os" in args) or ("with" in args) or (":" in args) or ("print" in args):
        raise ValueError()

    tmp = " ".join(args)
    tmp = tmp.replace("+", " + ")
    tmp = tmp.replace("-", " - ")
    tmp = tmp.replace("*", " * ")
    tmp = tmp.replace("/", " / ")
    nargs = []
    for v in tmp.split(" "):
        cur_tok = v
        for a in ("x", "y", "z", "sin", "cos", "tan", "cot"):
            if a not in cur_tok:
                continue
            pos = cur_tok.find(a)
            if len(cur_tok) >= pos + 1 and cur_tok[pos - 1].isalnum():
                cur_tok = cur_tok.replace(a, "*" + a)
            elif len(cur_tok) >= pos + 2 and cur_tok[pos + 1].isalnum():
                cur_tok = cur_tok.replace(a, a + "*")

        nargs.append(cur_tok)
    inp = " ".join(nargs)
    inp = inp.replace("{", "(")
    inp = inp.replace("[", "(")
    inp = inp.replace(".", "*")
    inp = inp.replace(",", ".")
    inp = inp.replace("^", "**")
    inp = inp.replace(")(", ")*(")
    inp = inp.replace("xy", "x*y")
    inp = inp.replace("xz", "x*z")
    inp = inp.replace("yx", "y*x")
    inp = inp.replace("yz", "y*z")
    inp = inp.replace("zx", "z*x")
    inp = inp.replace("zy", "z*y")
    return inp


class Meth(phoenix.Module):
    @phoenix.cmd_def(name="solve")
    def solve(self, ctx: phoenix.Context, args: list[str]) -> bool:
        inp = preproc_input(args)
        lhs, rhs = inp.split("=")
        try:
            if "=" in inp:
                solutions = eval(f"solve(Eq({lhs}, {rhs}))")
            else:
                solutions = eval(f"solve({inp})")
        except:
            ctx.reply("k hiu")
            raise
            return True
        sincos = ""
        if (
            ("sin" in inp)
            or ("cos" in inp)
            or ("tan" in inp)
            or ("cot" in inp)
            or ("pi" in inp)
            or ("π" in inp)
        ):
            # Simplify solutions with pi
            sincos = " (lược các chu kì tuần hoàn)"
            solutions = [nsimplify(i, [pi]) for i in solutions]
        fname = f"tmp/{random.randint(1, 999999)}.png"
        preview(solutions, viewer="file", filename=fname)
        img = Image.open(fname)
        im_new = pad_img(img, 30, 30, 30, 30, (255, 255, 255))
        im_new.save(fname)
        ctx.reply(f"có {len(solutions)} nghiệm" + sincos + ":", fname)
        return True

    @phoenix.cmd_def(name="simplify")
    def simplify(self, ctx: phoenix.Context, args: list[str]) -> bool:
        inp = preproc_input(args)
        try:
            solutions = nsimplify(
                inp,
                [
                    pi,
                ],
            )
        except:
            ctx.reply("k hiu")
            raise
            return True
        fname = f"tmp/{random.randint(1, 999999)}.png"
        preview(solutions, viewer="file", filename=fname)
        img = Image.open(fname)
        im_new = pad_img(img, 30, 30, 30, 30, (255, 255, 255))
        im_new.save(fname)
        ctx.reply("", fname)
        return True


def get(bot: phoenix.Bot) -> phoenix.Module:
    return Meth(bot)
