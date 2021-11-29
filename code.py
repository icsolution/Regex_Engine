class Regex:

    def match(self, pattern, string):
        pattern_1 = pattern
        if '?' in pattern or '*' in pattern or '+' in pattern:
            if '\\' not in pattern:
                pattern = self.check_repeat(pattern, string)
        pattern = pattern.replace('\\', '')
        if '^' in pattern_1 and '^' not in pattern:
            pattern = '^' + pattern
        if '$' in pattern_1 and '$' not in pattern:
            pattern += '$'
        if pattern.startswith('^') and pattern.endswith('$'):
            return pattern[1:-1] == string
        elif pattern.startswith('^'):
            pattern, string = pattern[1:], string[:len(pattern) - 1]
        elif pattern.endswith('$'):
            pattern, string = pattern[:-1], string[-(len(pattern) - 1):]
        return self.iterate(pattern, string)

    def iterate(self, pattern, string):
        for i in range(len(string) - len(pattern) + 1):
            if self.compare(pattern, string[i:i + len(pattern)]):
                return True
        return False

    @staticmethod
    def compare(pattern, string):
        if '\\' in pattern:
            pattern = pattern.replace('\\', '')
        if pattern and string:
            for i, j in zip(pattern, string):
                if i == j or i == '.':
                    continue
                else:
                    return False
            return True
        elif not pattern and not string or string:
            return True
        return False

    def check_repeat(self, pattern, string):
        for i in '?*+':
            if i in pattern:
                index = pattern.index(i)
                zero = pattern[:index - 1] + pattern[index + 1:]
                once = pattern.replace(i, '')
                if i == '?':
                    return zero if zero == string else once
                elif i == '*':
                    return zero if zero == string else self.repeat(pattern, string)
                else:
                    more = self.repeat(pattern, string)
                    return more
        return pattern

    @staticmethod
    def repeat(pattern, string):
        for i, j in enumerate(pattern):
            if j == '.':
                pattern = pattern.replace(j, string[i - 1])
            elif j in '^$':
                pattern = pattern.replace(j, '')
        index = pattern.index('*') if '*' in pattern else pattern.index('+')
        head = pattern[:index]
        tail = pattern[index + 1:]
        while head + head[-1] in string:
            head += head[-1]
        else:
            return head + tail


if __name__ == '__main__':
    re = Regex()
    target = input().split('|')
    result = re.match(*target)
    print(result)
