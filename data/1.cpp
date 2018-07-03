#include <bits/stdc++.h>

using namespace std;

typedef pair<int,int>   II;
typedef vector< II >      VII;
typedef vector<int>     VI;
typedef vector<long long>     VLL;
typedef vector< VI >    VVI;
typedef long long int   LL;

#define PB push_back
#define MP make_pair
#define F first
#define S second
#define SZ(a) (int)(a.size())
#define ALL(a) a.begin(),a.end()
#define SET(a,b) memset(a,b,sizeof(a))


#define din(n) int n; scanf("%d",&n)
#define dout(n) printf("%d\n",n)
#define llin(n) long long n; scanf("%lld",&n)
#define llout(n) printf("%lld\n",n)
#define strin(s,l) char s[l]; scanf("%s",s)
#define strout(n) printf("%s\n",n)
#define fast_io ios_base::sync_with_stdio(false);cin.tie(NULL)
#define endl '\n'

#define TRACE

#ifdef TRACE
#define trace(...) __f(#__VA_ARGS__, __VA_ARGS__)
template <typename Arg1>
void __f(const char* name, Arg1&& arg1){
        cerr << name << " : " << arg1 << '\n';
}
template <typename Arg1, typename... Args>
void __f(const char* names, Arg1&& arg1, Args&&... args){
        const char* comma = strchr(names + 1, ',');cerr.write(names, comma - names) << " : " << arg1<<" | ";__f(comma+1, args...);
}
#else
#define trace(...)
#endif
bool cmpManh(const std::pair<long long,long long>& l, const std::pair<long long,long long>& r)  {
return ((llabs(l.F) + llabs(l.S)) < (llabs(r.F) + llabs(r.S)));
}

int gcd(int a, int b){
if (a == 0) return b; return gcd(b%a, a); 
}

int main(void)
{
    return(0);
}