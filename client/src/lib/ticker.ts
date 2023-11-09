// async function fetch_ticker(ticker, ticks) {
//   const ticks_values = extractTickValues(ticks);
//   const json = await postData(ticks_values);
//   price = mapToPrice(json);
//   emas = mapToEmas(json, ticks);

import type { Time } from "lightweight-charts";

// }
type ChartData = {
  time: Time;
  value: number;
};

export function extractTickValues(ticks: [string, number][]) {
  return ticks.map((x) => x[1]);
}

export async function postData(
  ticker: string,
  interval: string,
  ticks_values: number[]
) {
  const res = await fetch(`/ticker`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ ticks: ticks_values, ticker, interval }),
  });
  return await res.json();
}

export function mapToPrice(json: any) {
  return json.map((x: any) => ({ time: x.datetime / 1000, value: x.Close }));
}

export function mapToEmas(json: any, ticks: [string, number][]) {
  let emas: { [key: string]: { color: string; data: ChartData[] } } = {};
  for (const [color, value] of ticks) {
    emas[value] = {
      color: color,
      data: json.map((x: any) => ({
        time: x.datetime / 1000,
        value: x[`${value}_ema`],
      })),
    };
  }
  return emas;
}

export function mapToMomentumOscilator(json: any, ticks: [string, number][]) {
  let emas: { [key: string]: { color: string; data: ChartData[] } } = {};
  for (const [color, value] of ticks) {
    emas[value] = {
      color: color,
      data: json.map((x: any) => ({
        time: x.datetime / 1000,
        value: x[`${value}_momentum`],
      })),
    };
  }
  emas["one"] = {
    color:"gray",
    data: json.map((x: any) => ({
      time: x.datetime / 1000,
      value: 1,
    })),
  }
  return emas;
}