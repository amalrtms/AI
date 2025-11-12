import copy

def is_var(x):
    return isinstance(x, str) and x[0].islower()

def occurs_check(var, x, theta):
    if var == x:
        return True
    if is_var(x) and x in theta:
        return occurs_check(var, theta[x], theta)
    if isinstance(x, tuple):
        return any(occurs_check(var, arg, theta) for arg in x[1])
    return False

def unify_terms(x, y, theta):
    if theta is None:
        return None
    if x == y:
        return theta
    if is_var(x):
        return unify_var(x, y, theta)
    if is_var(y):
        return unify_var(y, x, theta)
    return None

def unify_var(var, x, theta):
    if var in theta:
        return unify_terms(theta[var], x, theta)
    if is_var(x) and x in theta:
        return unify_terms(var, theta[x], theta)
    if occurs_check(var, x, theta):
        return None
    theta2 = theta.copy()
    theta2[var] = x
    return theta2

def unify_atom(a, b, theta=None):
    if theta is None:
        theta = {}
    if a[0] != b[0] or len(a[1]) != len(b[1]):
        return None
    for arg_a, arg_b in zip(a[1], b[1]):
        theta = unify_terms(arg_a, arg_b, theta)
        if theta is None:
            return None
    return theta

def subst_term(theta, t):
    if is_var(t):
        if t in theta:
            return subst_term(theta, theta[t])
        return t
    if isinstance(t, tuple):
        return (t[0], [subst_term(theta, a) for a in t[1]])
    return t

def subst_atom(theta, atom):
    return (atom[0], [subst_term(theta, a) for a in atom[1]])

def standardize_rule(rule, counter):
    premises, conclusion = rule
    mapping = {}
    suffix = f"_{counter}"
    def std_term(t):
        if is_var(t):
            if t not in mapping:
                mapping[t] = t + suffix
            return mapping[t]
        return t
    new_premises = []
    for p in premises:
        new_premises.append((p[0], [std_term(a) for a in p[1]]))
    new_conclusion = (conclusion[0], [std_term(a) for a in conclusion[1]])
    return new_premises, new_conclusion

def match_premises(premises, facts, theta=None, idx=0):
    if theta is None:
        theta = {}
    if idx == len(premises):
        return [theta]
    results = []
    p = premises[idx]
    for f in facts:
        theta2 = unify_atom(p, f, theta.copy())
        if theta2 is not None:
            results.extend(match_premises(premises, facts, theta2, idx+1))
    return results

def fol_fc_ask(kb_facts, kb_rules, query):
    facts = list(kb_facts)
    rules = list(kb_rules)
    counter = 0

    print("Initial facts:")
    for f in facts:
        print("  ", f)
    print("Query:", query, "\n")

    while True:
        new_facts = []
        for rule in rules:
            counter += 1
            premises, conclusion = standardize_rule(rule, counter)
            thetas = match_premises(premises, facts, {})
            for theta in thetas:
                inferred = subst_atom(theta, conclusion)
                if inferred not in facts and inferred not in new_facts:
                    print("Inferred", inferred, "from", premises, "with", theta)
                    new_facts.append(inferred)
                    phi = unify_atom(inferred, query, {})
                    if phi is not None:
                        print("\nQuery entailed with substitution:", phi)
                        return phi
        if not new_facts:
            print("\nQuery cannot be entailed.")
            return False
        facts.extend(new_facts)

# Example Knowledge Base
fact1 = ("Human", ["Socrates"])
kb_facts = [fact1]

rule1 = ([("Human", ["x"])], ("Mortal", ["x"]))  # Human(x) => Mortal(x)
kb_rules = [rule1]

query = ("Mortal", ["Socrates"])

fol_fc_ask(kb_facts, kb_rules, query)
