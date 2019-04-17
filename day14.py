import aoc


@aoc.test({
    '9': '5158916779',
    '5': '0124515891',
    '18': '9251071085',
    '2018': '5941429882',
})
def part_1(data: aoc.Data):
    num = int(data)
    mop, lop = 0, 1
    recipes = '37'
    while True:
        combined = int(recipes[mop]) + int(recipes[lop])
        recipes += str(combined)
        mop = (mop + 1 + int(recipes[mop])) % len(recipes)
        lop = (lop + 1 + int(recipes[lop])) % len(recipes)
        if len(recipes) > (num + 10):
            return recipes[num:num + 10]
