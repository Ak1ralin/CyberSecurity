# Guest Speaker From KPMG : Web Security
## GRC : The Strategy for Safety.
- The "GRC" Triad (The Strategy) : planning and checking the rules
    - **Gap Assessment (The "Checklist")**: A company looks at a list of safety best practices and checks off what they are actually doing. Anything unchecked is a gap they need to fix.
            
    - **Risk Assessment (The "Forecast")**: A company lists all the ways they could be hacked. They decide to spend their money fixing the most dangerous problems first, rather than trying to fix everything at once.

    - **IT Audit (The "Report")**: A specific type of accountant looks at a company’s computer systems to verify that the security tools are actually working and that the company isn't lying about how safe they are.
## Testing
- **Vulnerability Assessment (The "Evaluation")**: A systematic process to find known weaknesses.
- **Penetration Test (The "Attack")**: A manual, authorized simulated attack where a human expert (Ethical Hacker) tries to exploit the weaknesses found in the assessment.
    - Levels
        - **Black Box (The "Blind" Test):** Outsider without prior knowledge of the organization, or its systems.
        - **Grey Box:** Outsider with limited knowledge and valid credentials.
        - **White Box:** Insider with valid credentials and/or application source code.
        - **Threat Oriented:** Attacker with specific goal.
    - Pen Test Process : 4 Main Stages
        1. Setup
            - **1.1 Scope Definition:** The "Contract." You agree on what you are allowed to hack (the website?) and what is off-limits (the CEO's iPhone?).
            - **1.2 Information Gathering:** The "Stalking." The hacker Googles the company to find email addresses, employee names, or office locations.
        2. Recon
            - **2.1 Enumeration:** The "Knocking on Doors." The hacker checks which digital doors (ports) are open and what software is running behind them.
            - **2.2 Vulnerabilities Identification:** The "Spotting the Weakness." They find a specific door that has a broken lock (a software bug).
        3. Plan & Attack
            - **3.1 Result Analysis & Research:** The "Double Check." Before attacking, they confirm the broken lock is actually real and figure out which tool opens it.
            - **3.2 Exploitation:** The "Break-In." This is the actual hack. They enter the system and try to Escalate Privilege (go from a regular user to a "Super Admin" who controls everything).
        4. Clean up
            - **Analysis & Reporting:** The "Grade." The hacker writes a report explaining exactly how they broke in, how bad the damage could be, and—most importantly—how to fix it.
    - Pen Test Tools
        - **Kali Linux :** OS with 100+ hacking tool
        - **Nmap :** Network Scanner
        - **TheHarvester :** Automatic Search Machine
        - **DirBuster :** Hidden Page Finder (Tries 1,000+ possible hidden pages)
        - **BurpSuite :** Man in the Middle between browser and website.
        - **OWASP ZAP :** Free Opensource BurpSuite
        - **w3af :** Web Security Scanner
        - **SQLmap :** Automated SQL injection tool
        - **Metasploit :** Pre-made Attack Weapons, no need to code for attack
- **Red Teaming (The "Simulating")**: A full-scope, stealthy simulation of a real-world attack to test how well the company's defenders (The Blue Team) can detect and stop an attack.
## Attack Type
- **XSS (Cross-Site Scripting) :** Lets attacker run malicious code in the Victim's browser
    - **DOM-Based XSS :** Attacker sends Link -> Victim's Browser processes it improperly (Server is skipped/ignored)
    - **Reflected XSS :** Attacker sends Link -> Server reflects it -> Specific Victim (Who open link)
    - **Stored XSS :** Attacker saves code -> Server (Database) -> All Users (Everyone)
- **SQL Injection :** Input as query/command
    - Simple Detection : 
        - Opening/Closing string : ' single quote, " double quote
        - Boolean Condition : OR '1' = '1' --
        - String Concatenation : ||, +