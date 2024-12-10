# Keeping this here if  it turns out I need it after all


# Returns -1 if not related
# Returns 0 if if apstate1 is subset of apstate2
# Returns 1 if apstate2 is subset of apstate1 
def get_apstate_relation(apstate1, apstate2):
    ap1issub = True
    ap2issub = True
    for i in range(len(apstate1)):
        if apstate1[i] == "1" and apstate2[i] == "0":
            ap1issub = False
        if apstate1[i] == "0" and apstate2[i] == "1":
            ap2issub = False
    return 0 if ap1issub else 1 if ap2issub else -1

# Idea: remove superfluous apstates completely. e.g. if only sword is required, sword + chicken is unnecessary
print("Removing duplicate solutions")
for region in done_regions:
    if not region.location:
        continue
    parent_diffed_by_apstate = {}
    for parentName in region.parents:
        parent = regions_dict[parentName]
        if not parent.apstate in parent_diffed_by_apstate:
            parent_diffed_by_apstate[parent.apstate] = [parent]
        else:
            parent_diffed_by_apstate[parent.apstate].append(parent)
    # Remove subset apstates
    used_apstates = []
    for apstate_parents in parent_diffed_by_apstate.keys():
        if len(used_apstates) == 0:
            used_apstates.append(apstate_parents)
            continue
        new = True
        remove = []
        for used_apstate in used_apstates:
            if get_apstate_relation(apstate_parents, used_apstate) == 0:
                remove.append(used_apstate)
            if get_apstate_relation(apstate_parents, used_apstate) == 1:
                new = False
                break
        for rem in remove:
            used_apstates.remove(rem)
        if new:
            used_apstates.append(apstate_parents)

    for apstate in parent_diffed_by_apstate.keys():
        apstate_parents = parent_diffed_by_apstate[apstate]
        if not apstate in used_apstates:
            for parent in apstate_parents:
                parent.connections.remove(region.name)
                region.parents.remove(parent.name)
            continue
        if len(apstate_parents) > 1:
            best_parent = apstate_parents[0]
            best_complexity = best_parent.complexity
            for parent in apstate_parents[1:]:
                if parent.complexity >= best_complexity:
                    parent.connections.remove(region.name)
                    region.parents.remove(parent.name)
                else:
                    best_parent.connections.remove(region.name)
                    region.parents.remove(best_parent.name)
                    best_parent = parent
                    best_complexity = parent.complexity