Short Term
==========
1. Support for failed missions - requires adding a global dictionary.
1. What makes sense to add to the EDMC GUI?
1. Figure out what to do with faction states
1. Add Smuggling lever
1. Generate human-friendly text from daily plan.
1. Reload plans via timestamp (can use etag field in http head)
1. Detect war state for target faction, detect enemy
1. Add startdate field to plan
** 2. Massacre mission support <============= **


Mid Term
========
1. Implement Support for Elections
2. Upgrade button automatically installs new codebase

Long Term
=========
1. Accumulate contributions in a database somewhere
2. Graphs of progress, contributions, etc...
  
Problems?
=========
1. I don't see any indication of winning/losing conflict zones and FSS scenarios in the journal.

v 0.5 13 Dec 2020
=================
1. Add "conflictAlly" to plans.
2. Combat bond support
3. Chats that start with 'anticlub' or 'антиклуб' in an active system go to that system's discords
4. Add overview field to plan
5. Add notes field to plan


v 0.4 10 Dec 2020
=================
1. Bug fix
1. Research: Wars - how are events like CZ wins, Massacre Missions shown in journal

v 0.3 10 Dec 2020
=================
1. Save system address updates to local addresses.jsonl file.
2. Notify user when new version available.  Remove "Count Me" button.
3. Add support for outbreakCommodities.
4. Add support for blightCommodities.
5. Add support for draughtCommodities.
6. Add support for famineCommodities.
7. Add support for infrastructureCommodities.
8. Add support for terrorismCommodities.
9. Add support for naturalDisasterCommodities.
9. Remove click me stuff.

v 0.2 8 Dec 2020
================
1. Make download available via github distro.
1. Save sample DailyPlan as JSON(L).
1. Save sample DailyPlans as JSON(L).
1. Read plans from (remote) JSON(L) file.
1. Add reporters to loaded/downloaded dailyplans.
1. Check that 1st, 2nd DailyPlan work... 

v 0.1 7 Dec 2020
================
1. Move WebHook from DiscoReporter to DailyPlan, keep it as a list.
1. Add CMDR name to DiscordReporter output.
1. Empty targets dict on docking/jump.
1. Trade - check commodity.
1. Filter out trades to FleetCarriers.
1. Catch negative inf mission successes.
