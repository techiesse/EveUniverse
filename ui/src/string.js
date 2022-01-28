
export function splitS(s, n)
{
    const ret = []
    let i = 0
    while (i < s.length)
    {
        ret.push(s.substring(i, i + n))
        i += n
    }
    return ret
}

export function splitSL(s, n)
{
    const ret = []
    let i = 0
    const N = s.length
    while (i < N)
    {
        ret.push(s.substring(N - i, N - (i + n)))
        i += n
    }
    return ret.reverse()
}
