// Display relationships only: never expand a selection or invocation permission.
export function assignSkillFamilies(skills, families = []) {
  return skills.map(skill => {
    // Explicit documented membership wins over a broad presentation prefix.
    const family = families.find(row => [...(row.rootIds || []), ...(row.memberIds || [])].includes(skill.id))
      || families.find(row => (row.prefixes || []).some(prefix => skill.id.startsWith(prefix)));
    return family ? { ...skill, familyId: family.id, familyTitle: family.title, familyDescription: family.description,
      familyRelation: family.relation, familyRoot: (family.rootIds || []).includes(skill.id) } : skill;
  });
}
