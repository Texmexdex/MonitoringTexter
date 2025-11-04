# Trend Graphs Guide

Visual analysis of station readings over time to identify patterns, trends, and environmental factors.

## Overview

The Graphs feature provides:
- **Visual trend analysis** - See patterns at a glance
- **Time range filtering** - Focus on specific periods
- **Safe range overlay** - Quickly spot violations
- **Statistical analysis** - Key metrics and insights
- **Environmental correlation** - Track changes over time

## Accessing Graphs

1. Click **📈 Graphs** in the sidebar
2. Select a station from the dropdown
3. Choose a time range
4. View the trend graph and statistics

## Features

### 1. Station Selection

**Dropdown Menu:**
- Lists all configured stations
- Automatically selects first station
- Updates graph when changed

**Usage:**
- Select station to analyze
- Compare different stations
- Track individual station performance

### 2. Time Range Filters

**Available Ranges:**
- **Last 6 Hours** - Recent short-term trends
- **Last 24 Hours** - Daily patterns
- **Last 7 Days** - Weekly trends
- **Last 30 Days** - Monthly patterns
- **All Time** - Complete history

**Use Cases:**
- **6 Hours:** Immediate troubleshooting
- **24 Hours:** Daily cycle analysis
- **7 Days:** Weekly pattern detection
- **30 Days:** Long-term trend analysis
- **All Time:** Historical overview

### 3. Graph Display

**Elements:**
- **Blue Line** - Actual readings over time
- **Green Dashed Line** - Minimum safe value
- **Red Dashed Line** - Maximum safe value
- **Green Shaded Area** - Safe operating range
- **Data Points** - Individual readings (circles)

**Interpretation:**
- Points in green area = Normal
- Points above red line = Too high
- Points below green line = Too low
- Line slope = Rate of change
- Flat line = Stable readings
- Oscillating = Cyclical pattern

### 4. Statistics Panel

**Displayed Metrics:**
- **Total Readings** - Number of data points
- **Time Span** - Duration covered
- **First/Last Reading** - Time range boundaries
- **Average** - Mean value
- **Minimum** - Lowest reading
- **Maximum** - Highest reading
- **Safe Range** - Configured limits
- **Alerts** - Count and percentage
- **Normal** - Count and percentage

**Usage:**
- Quick overview of station performance
- Identify alert frequency
- Spot outliers
- Assess stability

### 5. Show Safe Range Toggle

**Checkbox Control:**
- ☑ Checked - Shows min/max lines and shaded area
- ☐ Unchecked - Shows only readings

**When to Disable:**
- Comparing multiple time periods
- Focusing on trend shape
- Analyzing rate of change
- Cleaner visualization

## Use Cases

### 1. Troubleshooting Alerts

**Scenario:** Station triggering frequent alerts

**Steps:**
1. Select the station
2. Choose "Last 24 Hours"
3. Look for patterns:
   - Sudden spikes?
   - Gradual drift?
   - Cyclical variations?
   - Time-of-day correlation?

**Insights:**
- **Sudden spike** → Equipment malfunction
- **Gradual drift** → Calibration issue
- **Cyclical** → Environmental factor
- **Time-based** → Operational pattern

### 2. Environmental Correlation

**Scenario:** Readings vary with weather/temperature

**Steps:**
1. Select "Last 7 Days"
2. Note reading patterns
3. Compare with weather data
4. Identify correlations

**Examples:**
- Higher readings during hot days
- Lower readings at night
- Spikes during rain
- Patterns with humidity

**Actions:**
- Adjust safe ranges seasonally
- Account for environmental factors
- Improve insulation/protection
- Schedule maintenance accordingly

### 3. Trend Analysis

**Scenario:** Long-term performance monitoring

**Steps:**
1. Select "Last 30 Days" or "All Time"
2. Observe overall trend
3. Identify patterns
4. Plan preventive maintenance

**Patterns:**
- **Upward trend** → Degradation, needs attention
- **Downward trend** → Improvement or issue
- **Stable** → Good performance
- **Increasing variance** → Instability developing

### 4. Comparing Time Periods

**Scenario:** Before/after maintenance comparison

**Steps:**
1. Note maintenance date/time
2. View "Last 30 Days"
3. Compare readings before and after
4. Assess improvement

**Metrics:**
- Alert frequency change
- Average value shift
- Variance reduction
- Stability improvement

### 5. Identifying Cycles

**Scenario:** Detecting daily/weekly patterns

**Steps:**
1. Select "Last 7 Days"
2. Look for repeating patterns
3. Note timing of peaks/valleys
4. Correlate with operations

**Common Cycles:**
- **Daily:** Temperature, usage patterns
- **Weekly:** Operational schedules
- **Monthly:** Seasonal changes
- **Irregular:** Equipment issues

## Interpreting Graphs

### Healthy Station

**Characteristics:**
- Readings mostly in green zone
- Stable trend line
- Low variance
- Few or no alerts
- Predictable patterns

**Example:**
```
Value
  │
75├─────────────────────── Max
  │     ●  ●  ●  ●  ●
  │   ●          ●      ●
50├─ ●                    ● Normal Range
  │
25├─────────────────────── Min
  │
  └─────────────────────────> Time
```

### Warning Signs

**Upward Drift:**
```
Value
  │              ●  ●  ●
75├───────────●──────────── Max
  │        ●
  │     ●
50├──●──────────────────── Normal
  │
  └─────────────────────────> Time
```
**Action:** Investigate cause, adjust if needed

**High Variance:**
```
Value
  │     ●           ●
75├─────────────────────── Max
  │  ●     ●     ●
50├────●─────●──────────── Normal
  │           ●
25├─────────────────────── Min
  └─────────────────────────> Time
```
**Action:** Check for instability, environmental factors

**Frequent Alerts:**
```
Value
  │  ●        ●        ●
75├─────────────────────── Max (Exceeded)
  │     ●  ●     ●  ●
50├─────────────────────── Normal
  │
  └─────────────────────────> Time
```
**Action:** Adjust ranges or fix equipment

### Seasonal Patterns

**Summer vs Winter:**
```
Summer (Hot):
Value
  │        ●  ●  ●  ●
75├────────────────────── Max
  │     ●
50├──●──────────────────── Normal
  │
  └────────────────────────> Time

Winter (Cold):
Value
  │
75├─────────────────────── Max
  │
50├─────────────────────── Normal
  │     ●  ●  ●  ●
25├──●──────────────────── Min
  └────────────────────────> Time
```
**Action:** Consider seasonal range adjustments

## Best Practices

### Regular Monitoring

**Daily:**
- Check "Last 24 Hours" for each station
- Look for unusual patterns
- Note any alerts

**Weekly:**
- Review "Last 7 Days"
- Identify trends
- Compare week-over-week

**Monthly:**
- Analyze "Last 30 Days"
- Assess long-term performance
- Plan maintenance

### Documentation

**Record Observations:**
- Screenshot interesting patterns
- Note correlations discovered
- Document maintenance impacts
- Track seasonal changes

**Use Cases:**
- Training new staff
- Troubleshooting reference
- Performance reports
- Compliance documentation

### Correlation Analysis

**Environmental Factors:**
- Temperature
- Humidity
- Pressure
- Weather events

**Operational Factors:**
- Usage patterns
- Maintenance schedules
- Equipment changes
- Process modifications

**Track:**
- When readings spike
- What changed recently
- External conditions
- Operational events

## Advanced Tips

### Spotting Equipment Issues

**Gradual Degradation:**
- Slow upward or downward trend
- Increasing variance over time
- More frequent alerts

**Sudden Failure:**
- Abrupt change in readings
- Flat line (sensor failure)
- Extreme values

**Calibration Drift:**
- Consistent offset from normal
- Gradual shift over weeks
- Stable but wrong values

### Optimizing Safe Ranges

**Too Tight:**
- Frequent false alerts
- Readings often at boundaries
- High alert percentage

**Too Loose:**
- Missing real issues
- No alerts when problems exist
- Wide variance accepted

**Just Right:**
- Alerts only for real issues
- Most readings comfortably in range
- Clear margin for normal variation

### Predictive Maintenance

**Use Graphs To:**
- Predict when maintenance needed
- Schedule before failure
- Track maintenance effectiveness
- Optimize intervals

**Indicators:**
- Increasing trend toward limits
- Growing variance
- More frequent alerts
- Pattern changes

## Troubleshooting

### No Data Displayed

**Check:**
- Station has readings in database
- Time range includes data
- Station is selected (not "Select Station")

**Solution:**
- Submit test readings
- Choose "All Time" range
- Verify station configuration

### Graph Not Updating

**Check:**
- Click "🔄 Refresh" button
- Change time range
- Reselect station

**Solution:**
- Manual refresh
- Check for new readings
- Restart application if needed

### Timestamps Incorrect

**Check:**
- System clock is correct
- Timezone settings
- Database timestamps

**Solution:**
- Correct system time
- Readings use system time when submitted
- Historical data keeps original timestamps

### Performance Issues

**Large Datasets:**
- Use shorter time ranges
- Limit to specific periods
- Archive old data

**Slow Rendering:**
- Reduce data points
- Close other applications
- Upgrade hardware if needed

## Export and Reporting

### Screenshots

**Capture Graphs:**
1. Set desired time range
2. Position graph as needed
3. Use Windows Snipping Tool (Win+Shift+S)
4. Save for reports

**Use For:**
- Performance reports
- Troubleshooting documentation
- Training materials
- Compliance records

### Data Export (Future)

**Planned Features:**
- Export to CSV
- Export to Excel
- PDF reports
- Automated reports

## Summary

The Graphs feature provides powerful visual analysis to:
- ✅ Identify trends and patterns
- ✅ Spot environmental correlations
- ✅ Troubleshoot issues quickly
- ✅ Plan preventive maintenance
- ✅ Optimize safe ranges
- ✅ Document performance
- ✅ Train staff effectively

Use graphs regularly to maintain optimal station performance and catch issues early!
