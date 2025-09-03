// /public/js/pricing-lib.js
export function formatEUR(x){ return new Intl.NumberFormat('es-ES',{style:'currency',currency:'EUR'}).format(x); }

export function pricePerSeatFromTiers(n, tiers){
  for (const t of tiers) if (n <= t.maxSeats) return t.price;
  return tiers[tiers.length - 1].price;
}

export function computeTeamMonthly(n, tiers){ 
  const seat = pricePerSeatFromTiers(n, tiers);
  return { seat, total: seat * n };
}

export function computeAnnual(totalMonthly, annualDiscount){ 
  const yearly = totalMonthly * 12 * (1 - annualDiscount); 
  return { yearly, monthlyEq: yearly / 12 };
}
