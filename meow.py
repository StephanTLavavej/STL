clOptions = [
    'cl',
    '/EHsc',
    '/nologo',
    '/W4',
    '/std:c++latest',
    '/Zc:preprocessor',
    '/MD',
    '/Od',
    '/D_SILENCE_ALL_CXX17_DEPRECATION_WARNINGS',
    '/exportHeader',
    '/headerName:angle',
    '/translateInclude',
]

def headerList():
    stlHeaders = [
        'algorithm',
        'any',
        'array',
        'atomic',
        'barrier',
        'bit',
        'bitset',
        'charconv',
        'chrono',
        'codecvt',
        'compare',
        'complex',
        'concepts',
        'condition_variable',
        'coroutine',
        'deque',
        'exception',
        'execution',
        'filesystem',
        'format',
        'forward_list',
        'fstream',
        'functional',
        'future',
        'initializer_list',
        'iomanip',
        'ios',
        'iosfwd',
        'iostream',
        'istream',
        'iterator',
        'latch',
        'limits',
        'list',
        'locale',
        'map',
        'memory_resource',
        'memory',
        'mutex',
        'new',
        'numbers',
        'numeric',
        'optional',
        'ostream',
        'queue',
        'random',
        'ranges',
        'ratio',
        'regex',
        'scoped_allocator',
        'semaphore',
        'set',
        'shared_mutex',
        'source_location',
        'span',
        'sstream',
        'stack',
        'stdexcept',
        'stop_token',
        'streambuf',
        'string_view',
        'string',
        'strstream',
        'syncstream',
        'system_error',
        'thread',
        'tuple',
        'type_traits',
        'typeindex',
        'typeinfo',
        'unordered_map',
        'unordered_set',
        'utility',
        'valarray',
        'variant',
        'vector',
        'version',
    ]

    # header-units.json
    headerUnitsJsonList = [
        # '__msvc_all_public_headers.hpp', # for testing, not production
        '__msvc_system_error_abi.hpp',
        '__msvc_tzdb.hpp',
        'algorithm',
        'any',
        'array',
        'atomic',
        'barrier',
        'bit',
        'bitset',
        # 'cassert', # design is permanently incompatible with header units
        # 'ccomplex', # removed in C++20
        'cctype',
        'cerrno',
        'cfenv',
        'cfloat',
        'charconv',
        'chrono',
        'cinttypes',
        # 'ciso646', # removed in C++20
        'climits',
        'clocale',
        'cmath',
        'codecvt',
        'compare',
        'complex',
        'concepts',
        'condition_variable',
        'coroutine',
        'csetjmp',
        'csignal',
        # 'cstdalign', # removed in C++20
        'cstdarg',
        # 'cstdbool', # removed in C++20
        'cstddef',
        'cstdint',
        'cstdio',
        'cstdlib',
        'cstring',
        # 'ctgmath', # removed in C++20
        'ctime',
        'cuchar',
        'cwchar',
        'cwctype',
        'deque',
        'exception',
        'execution',
        'filesystem',
        'format',
        'forward_list',
        'fstream',
        'functional',
        'future',
        # 'hash_map', # non-Standard, will be removed soon
        # 'hash_set', # non-Standard, will be removed soon
        'initializer_list',
        'iomanip',
        'ios',
        'iosfwd',
        'iostream',
        'iso646.h',
        'istream',
        'iterator',
        'latch',
        'limits',
        'list',
        'locale',
        'map',
        'memory',
        'memory_resource',
        'mutex',
        'new',
        'numbers',
        'numeric',
        'optional',
        'ostream',
        'queue',
        'random',
        'ranges',
        'ratio',
        'regex',
        'scoped_allocator',
        'semaphore',
        'set',
        'shared_mutex',
        'source_location',
        'span',
        'sstream',
        'stack',
        'stdexcept',
        'stop_token',
        'streambuf',
        'string',
        'string_view',
        'strstream',
        'syncstream',
        'system_error',
        'thread',
        'tuple',
        'type_traits',
        'typeindex',
        'typeinfo',
        'unordered_map',
        'unordered_set',
        'use_ansi.h',
        'utility',
        'valarray',
        'variant',
        'vector',
        # 'version', # importable, but provides feature-test macros only, which can control header inclusion
        'xatomic.h',
        'xatomic_wait.h',
        'xbit_ops.h',
        'xcall_once.h',
        'xcharconv.h',
        'xcharconv_ryu.h',
        'xcharconv_ryu_tables.h',
        'xerrc.h',
        'xfacet',
        'xfilesystem_abi.h',
        'xhash',
        'xiosbase',
        # 'xkeycheck.h', # internal header, provides no machinery, scans for macroized keywords only
        'xlocale',
        'xlocbuf',
        'xlocinfo',
        'xlocinfo.h',
        'xlocmes',
        'xlocmon',
        'xlocnum',
        'xloctime',
        'xmemory',
        'xnode_handle.h',
        'xpolymorphic_allocator.h',
        'xsmf_control.h',
        'xstddef',
        'xstring',
        'xthreads.h',
        'xtimec.h',
        'xtr1common',
        'xtree',
        'xutility',
        'ymath.h'
        # 'yvals.h', # internal header, provides macros that control header inclusion
        # 'yvals_core.h' # internal header, provides macros that control header inclusion
    ]

    return sorted(set(stlHeaders + headerUnitsJsonList))

import subprocess
compilerOutput = subprocess.run(clOptions + ['/sourceDependencies:directives', '-'] + headerList(),
    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

def decodeJsonObjects(str):
    jsonObjects = []

    from json import JSONDecoder
    jsonDecoder = JSONDecoder()

    idx = 0
    strLen = len(str)

    while idx < strLen:
        obj, idx = jsonDecoder.raw_decode(str, idx)
        jsonObjects.append(obj)

    return jsonObjects

jsonObjects = decodeJsonObjects(compilerOutput.stdout)

def getFilename(str):
    return str[str.rfind('\\') + 1:]

remainingDependencies = {}

for jsonObject in jsonObjects:
    hdr = getFilename(jsonObject['Data']['Source'])
    dep = [getFilename(hdr) for hdr in jsonObject['Data']['ImportedHeaderUnits']]
    remainingDependencies[hdr] = dep

builtHeaderUnits = []

while len(remainingDependencies) > 0:
    readyToBuild = [hdr for hdr, dep in remainingDependencies.items() if len(dep) == 0]
    extraOptions = ['/Fo', '/MP']
    extraOptions.append('/wd5106') # TRANSITION, VSO-1329976
    for hdr in builtHeaderUnits:
        extraOptions += ['/headerUnit:angle', f'{hdr}={hdr}.ifc']
    commandLine = clOptions + extraOptions + readyToBuild
    print(' '.join(commandLine))
    subprocess.run(commandLine)
    remainingDependencies = {
        hdr: [d for d in dep if d not in readyToBuild]
        for hdr, dep in remainingDependencies.items() if len(dep) > 0
    }
    builtHeaderUnits += readyToBuild
