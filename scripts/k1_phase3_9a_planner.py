"""Frozen debt planning plus two observed author prompt patterns only."""
import re
from k1_phase3_9_planner import health,debt_candidates,proposals
from k1_phase3_9_planner import contract as old_contract, author_findings as old_findings, GAPS as OLD_GAPS
GAPS={**OLD_GAPS,'불다':{'avoid':'밖에는 비하고 바람이 있어요','strategy':'omit wind when 불다 is unavailable; 밖에는 비가 많이 와요'},'written_message':{'avoid':'종이에 말을 써요','strategy':'omit object; 종이에 써요 and show message with a direct quotation'}}
def author_findings(text,intended_pack=False):
    xs=old_findings(text,intended_pack)
    if re.search(r'비하고\s*바람이\s*있',text):xs.append({'category':'naturalness','key':'wind_existential_substitution','strategy':GAPS['불다']['strategy']})
    if re.search(r'종이에\s*말을\s*써',text):xs.append({'category':'naturalness','key':'written_message_substitution','strategy':GAPS['written_message']['strategy']})
    return xs
def contract(f,snapshot):
    from k1_author_contract import SCHEMA,template
    c=old_contract(f,snapshot);c['KNOWN_GAPS']=GAPS
    c['AUTHOR_SELFCHECK_SCHEMA']=str(SCHEMA);c['AUTHOR_SELFCHECK_TEMPLATE']=template()
    return c
