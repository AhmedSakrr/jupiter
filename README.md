# Jupiter
> internet relay chat botnet for efnet

## Information
Jupiter will create a botnet by connecting a defined number of clones to every EFNet server. A single host could potentially create close to 100 clones without any suspicion. It is meant to monitor/jupe/hold nicks & be controlled to do just about anything.

For example, at the time of writing this, there are 14 active EFNet servers. With 3 clones per-server on IPv4 connections, plus another 3 clones per-server on IPv6 connections, thats 6 clones per-server, equating to 84 total clones...all from a single machine. Run this bot on multiple machines, you get the point.

Any server with SSL/TLS ports opened, will be connected using SSL/TLS. If using SSL/TLS to connect fails, it will fall back to a standard connection on port 6667 and will try an SSL/TLS again next time. When IPv6 is enabled, Servers with IPv6 support will be connected to with both IPv4 & IPv6 clones. Juping is handling using [MONITOR](https://ircv3.net/specs/extensions/monitor) & by watching for nick changes or quits.

The bot is designed to be very minimal, secure, & trustless by nature. This means anyone can run a copy of your script on their server to help build your botnet.

It is highly recommended that you use a [random spoofing ident protocol daemon](https://github.com/acidvegas/random/blob/master/irc/identd.py)

## Commands
| Command                 | Description                                                                                               |
| ----------------------- | --------------------------------------------------------------------------------------------------------- |
| 5000 \<chan>            | Emulates SuperNETs #5000 channel *(Joins \<chan> and will PM bomb anyone who joins the channel)*          |
| id                      | Send bot identity                                                                                         |
| raw [-d] \<data>        | Send \<data> to server, optionally delayed with -d argument                                               |
| relay \<chan>           | Relay all data from \<chan> into the bot channel *(Can not use @all & must join channel via `raw` first)* |
| relay stop              | Stop the relay *(Will not turn off from kicks, etc)*                                                      |
| monitor list            | Return MONITOR list                                                                                       |
| monitor reset           | Reset MONITOR list                                                                                        |
| monitor \<+/->\<nicks>  | Add (+) or Remove (-) \<nicks> from MONITOR list. *(Can be a single nick or comma seperated list)*        |

**Note:** All commands must be prefixed with @all or the bots nick & will work in a channel or private message.

Raw data must be IRC RFC compliant data & any nicks in the MONITOR list will be juped as soon as they become available.

## Todo
- CTCP replies *(Randomized but persistent on a per-bot basis)*
- Built in identd server with randomized spoofing responses
- Fake conversation mode in the bot channel to look legit incase network operators come sniffing around
- Takeover features to automatitically jupe a channel when you get +o
- Protection features *(Automatically +o other bots, remove bans on bots, set many +eI modes, etc)*

## Mirrors
- [acid.vegas](https://git.acid.vegas/jupiter)
- [GitHub](https://github.com/acidvegas/jupiter)
- [GitLab](https://gitlab.com/acidvegas/jupiter)
- [SuperNETs](https://git.supernets.org/acidvegas/jupiter)