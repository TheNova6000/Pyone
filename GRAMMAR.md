Program       → Statement+
Statement     → Declaration
              | Assignment
              | Print
              | IfBlock

Declaration   → "let" Identifier ("is" | "be") Expression
Assignment    → Identifier ("is" | "be") Expression
Print         → "print" Expression

IfBlock       → "if" Condition
                 Statement*
                 ("otherwise" Condition Statement*)*
                 ("else" Statement*)?
                 "end"

Expression    → Operand (Operator Operand)*

Operator      → + | - | * | / | > | < | >= | <= | ==