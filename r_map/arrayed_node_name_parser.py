import re
from typing import Callable, Tuple, Optional, Any, List, Iterable
from functools import partial

leading_zero_re = re.compile(r'0*(\d+)')
ParseMatch = Optional[Tuple[Any,str]]

def parse_fixed_width_leading_zero_int(fixed_width:int, s:str) -> ParseMatch:
    if fixed_width == 0:
        raise ValueError("Expecting non zero integer for fixed_width")

    if len(s) < fixed_width:
        return None

    to_parse = s[:fixed_width]
    m = leading_zero_re.match(to_parse)
    if m:
        if fixed_width and m.end() != fixed_width:
            return None
        return int(m.group(1)), s[fixed_width:]
    return None

def parse_leading_zero_int(s:str) -> ParseMatch:
    m = leading_zero_re.match(s)
    if m:
        return int(m.group(1)), s[m.end():] # (int, remaining)
    return None

def parse_substring_match(sub_re, s:str) -> ParseMatch:
    m = sub_re.match(s)
    if m:
        return True, s[m.end():]
    else:
        return None

def gen_fixed_width_int(width:int, val:int):
    return f'{val:0{width}}'

def make_parser_helper(index_matches:List[re.Match], s) -> Iterable[Callable]:
    current_index = 0
    for m in index_matches:
        start, end = m.span()
        width = end - start - 2
        if start > current_index:
            sub_str = s[current_index:start]
            yield sub_str, partial(parse_substring_match, re.compile(re.escape(sub_str)))
        if width > 1:
            yield partial(gen_fixed_width_int, width), partial(parse_fixed_width_leading_zero_int, width)
        else:
            yield str, parse_leading_zero_int
        current_index = end
    if current_index != len(s):
        sub_str = s[current_index:]
        yield partial(parse_substring_match, re.compile(re.escape(sub_str)))

def name_parser(parsers:List[Callable], name:str) -> Optional[int]:
    ints = []
    remaining = name
    for p in parsers:
        res = p(remaining)
        if res:
            val, remaining = res
            if isinstance(val, bool):
                if not val:
                    return None
            elif isinstance(val, int):
                ints.append(val)
        else:
            return None
    s_ints = set(ints) #these integers should all match the same value
    if len(s_ints) != 1:
        return None
    else:
        return s_ints.pop()

def name_gen_helper(gens, index:int) -> Iterable[str]:
    for g in gens:
        if isinstance(g, str):
            yield g
        else:
            yield g(index)

def make_parser(index_range:range, array_letter:str, name_spec:str) -> Callable:
    index_re = re.compile(rf'\[{array_letter}+\]')
    name_sans_index = index_re.sub('', name_spec)
    if '[' in name_sans_index or ']' in name_sans_index:
        raise ValueError(f"couldn't parse name: {name}")
    name_gens, sub_parsers = zip(*make_parser_helper(index_re.finditer(name_spec), name_spec))

    def name_gen(index:int) -> str:
        return ''.join(name_gen_helper(name_gens, index))

    # Unfortunately, this isn't a fully robust parser and will fail for names of
    # this form: register[n]02b because the regex for the integer is greedy and
    # a lookahead/retry mechanism hasn't been added. Since this is an unlikely
    # usage, the basic approach will do as the alternative of bringing in a more
    # fully fledged parser (and the associatated dependency) is not attractive.

    def parser(name:str) -> Optional[int]:
        possible_index = name_parser(sub_parsers, name)
        #possible index used as a boolean initially and as an integer at the end
        if (possible_index is not None) and (possible_index in index_range):
            return possible_index
        else:
            return None
    return name_gen, parser
