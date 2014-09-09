import random, regex

from tornado.web import RequestHandler

from homeweb.config import get_config
from homeweb.util import get_random_uid
from homeweb.util import apply_template, write_return


class InvalidDiceExpressionException(ValueError):
    pass

class DicerollHandler(RequestHandler):
    def display_dice_session(self, sessionid=None, error=None):
        session = DiceSession.get_cached_session(sessionid)
        if sessionid and not session:
            self.write_error(404)
            return

        return {'error': error, 'session': session, 'float': float}

    @write_return
    @apply_template("demos/diceroll.html")
    def get(self, sessionid=None):
        return self.display_dice_session(sessionid)

    @write_return
    @apply_template("demos/diceroll.html")
    def post(self, sessionid=None):
        if self.get_argument("new-session") == "true":
            rollspec = self.get_argument("dice-input")
            rollcomm = self.get_argument("comment", "")
            try:
                diceroll = DiceRoll(rollspec, rollcomm)
            except InvalidDiceExpressionException as e:
                self.display_dice_session(self, error=' '.join(e.args))
            diceroll.do_roll()

            session = DiceSession()
            session.add_roll(diceroll)
            session.save()

            prefix = '' if self.request.path.endswith('/') else 'dice/'
            self.redirect(prefix+session.uid)
            return
        self.write_error(403)

class DiceSession(object):
    @staticmethod
    def make_cache_key(uid):
        return "DiceSession++"+str(uid)
    @staticmethod
    def get_cached_session(uid):
        cache = get_config().get_memcache_client()
        cache_key = DiceSession.make_cache_key(uid)
        return cache.get(cache_key)

    def __init__(self):
        self.uid = get_random_uid(lambda x: DiceSession.get_cached_session(x)==None)
        self.rolls = []
        self.save()

    def save(self):
        cache = get_config().get_memcache_client()
        cache_key = DiceSession.make_cache_key(self.uid)
        cache.set(cache_key, self)

    def add_roll(self, diceroll):
        self.rolls.append(diceroll)

class DiceRoll(object):
    DICE_REGEX = regex.compile("\A([0-9]+d[0-9]+)([+-][0-9]+(?:d[0-9]+)?)*\Z")
    @staticmethod
    def roll_dice(num_dice, num_sides):
        num_dice = int(num_dice)
        num_sides = int(num_sides)
        if num_dice < 1:
            raise ValueError("Number of dice less than 0", num_dice)
        if num_sides < 1:
            raise ValueError("Number of sides less than 0", num_sides)
        rolls = [random.randint(1, num_sides) for i in range(num_dice)]
        return rolls

    def __init__(self, rolldef, comment=""):
        #Clear whitespace
        self.rolldef_dirty = rolldef
        self.rolldef = regex.split('[ \r\n\t]', rolldef)
        self.rolldef = ''.join(self.rolldef).lower()

        self.comment = comment

        self.rolls = []
        self.roll_results = []
        self.roll_total = 0
        self.parse()
        self.do_roll()

    def parse(self):
        match = DiceRoll.DICE_REGEX.search(self.rolldef)
        if not match:
            raise InvalidDiceExpressionException("Invalid dice", self.rolldef)
        firstroll = '+' + match.captures(1)[0]
        self.rolls = [firstroll] + match.captures(2)
        return self.rolls

    @property
    def roll(self):
        if not self.roll_results:
            self.do_roll()
        return self.roll_total, self.roll_min, self.roll_max, self.roll_results

    def do_roll(self, reroll=False):
        if not reroll and self.roll_results:
            return
        self.roll_results = []

        for roll_exp in self.rolls:
            roll_entry = {}
            roll_entry['roll_exp'] = roll_exp
            roll_sign = roll_exp[0]
            if "d" in roll_exp:
                num_dice, num_sides = roll_exp[1:].split("d")
                roll_entry['num_dice'] = int(num_dice)
                roll_entry['num_sides'] = int(num_sides)
                dice_rolls = DiceRoll.roll_dice(num_dice, num_sides)
                roll_entry['rolls'] = dice_rolls
                roll_entry['min'] = roll_entry['num_dice']
                roll_entry['max'] = roll_entry['num_dice'] * roll_entry['num_sides']
            else:
                # Constant value
                roll_entry['num_dice'] = 0
                roll_entry['num_sides'] = 0
                roll_entry['rolls'] = []
                dice_rolls = [int(roll_exp[1:])]
                roll_entry['min'] = dice_rolls[0]
                roll_entry['max'] = dice_rolls[0]
            roll_entry['value'] = sum(dice_rolls) * {'+':1,'-':-1}[roll_sign]
            self.roll_results.append(roll_entry)

        self.roll_total = sum([entry['value'] for entry in self.roll_results])
        self.roll_min = sum([entry['min'] for entry in self.roll_results])
        self.roll_max = sum([entry['max'] for entry in self.roll_results])

