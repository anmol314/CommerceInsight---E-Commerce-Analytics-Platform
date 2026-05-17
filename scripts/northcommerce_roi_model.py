"""
northcommerce_roi_model.py
Win-back ROI deterministic model and Monte Carlo simulation.
Saves: winback_results.csv, winback_mc_summary.csv, winback_scenarios.csv
"""
import argparse
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import beta, norm

class WinBackModel:
    def __init__(self, aov=800.0, margin=0.15, cost_per_user=50.0, base_reactivation=0.10, avg_orders_per_reactivated=1.4):
        self.aov = aov
        self.margin = margin
        self.cost_per_user = cost_per_user
        self.base_reactivation = base_reactivation
        self.avg_orders_per_reactivated = avg_orders_per_reactivated

    def run(self, lost_customers:int, horizon_days:int=30):
        recovered = lost_customers * self.base_reactivation
        expected_orders = recovered * self.avg_orders_per_reactivated
        gm = expected_orders * self.aov
        gross_margin = gm * self.margin
        cost = recovered * self.cost_per_user
        roi = gross_margin / cost if cost>0 else np.nan
        payback_days = (cost / (gross_margin / horizon_days)) if gross_margin>0 else np.nan
        return {
            'lost_customers': lost_customers,
            'recovered_customers': recovered,
            'expected_orders': expected_orders,
            'gmv': gm,
            'gross_margin': gross_margin,
            'cost': cost,
            'roi': roi,
            'payback_days': payback_days
        }

class MonteCarlo:
    def __init__(self, model:WinBackModel, sims=10000):
        self.model = model
        self.sims = sims

    def run(self, lost_customers:int):
        # draw reactivation from Beta around base_reactivation
        a = max(1, int(self.model.base_reactivation*100))
        b = max(1, 100 - a)
        reactivation = beta.rvs(a, b, size=self.sims)
        aov_samples = norm.rvs(loc=self.model.aov, scale=self.model.aov*0.1, size=self.sims)
        orders_samples = norm.rvs(loc=self.model.avg_orders_per_reactivated, scale=0.5, size=self.sims)

        results = []
        for i in range(self.sims):
            rec = lost_customers * reactivation[i]
            exp_orders = rec * max(0.1, orders_samples[i])
            gmv = exp_orders * max(1.0, aov_samples[i])
            gross_margin = gmv * self.model.margin
            cost = rec * self.model.cost_per_user
            roi = gross_margin / cost if cost>0 else np.nan
            results.append({'roi': roi, 'gmv': gmv, 'gross_margin': gross_margin, 'cost': cost})
        df = pd.DataFrame(results)
        summary = df.quantile([0.01,0.05,0.25,0.5,0.75,0.95,0.99])
        return df, summary


def scenario_comparison(lost_customers, model:WinBackModel):
    scenarios = {
        'Base': dict(model.__dict__),
        'Conservative': dict(model.__dict__, base_reactivation=max(0.01, model.base_reactivation*0.6), aov=model.aov*0.9),
        'Optimistic': dict(model.__dict__, base_reactivation=min(0.8, model.base_reactivation*1.6), aov=model.aov*1.1),
        'No Incentive': dict(model.__dict__, base_reactivation=max(0.0, model.base_reactivation*0.2))
    }
    rows = []
    for name, params in scenarios.items():
        m = WinBackModel(**params)
        res30 = m.run(lost_customers, horizon_days=30)
        res60 = m.run(lost_customers, horizon_days=60)
        rows.append({'scenario':name,'horizon_30_roi':res30['roi'],'horizon_60_roi':res60['roi'],'gmv_30':res30['gmv']})
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lost-customers', type=int, default=1000)
    parser.add_argument('--outdir', default=str(Path(__file__).resolve().parents[1] / 'outputs'))
    args = parser.parse_args()
    out = Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    model = WinBackModel()
    det = model.run(args.lost_customers)
    pd.DataFrame([det]).to_csv(out / 'winback_results.csv', index=False)

    mc = MonteCarlo(model)
    df_mc, summary = mc.run(args.lost_customers)
    df_mc.to_csv(out / 'winback_mc_raw.csv', index=False)
    summary.to_csv(out / 'winback_mc_summary.csv')

    scenarios = scenario_comparison(args.lost_customers, model)
    scenarios.to_csv(out / 'winback_scenarios.csv', index=False)
    print(f'Saved deterministic, MC and scenario outputs to {out}')

if __name__ == '__main__':
    main()
