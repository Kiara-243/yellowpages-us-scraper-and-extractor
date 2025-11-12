# Yellowpages US Scraper and Extractor
The Yellowpages US Scraper and Extractor is a high-performance tool designed to gather complete business details from Yellow Pages with precision and speed. It simplifies lead generation by automating the extraction of names, contacts, reviews, and other essential attributes. This scraper helps users collect verified business information at scale for marketing, research, and sales.


<p align="center">
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://github.com/za2122/footer-section/blob/main/media/scraper.png" alt="Bitbash Banner" width="100%"></a>
</p>
<p align="center">
  <a href="https://t.me/devpilot1" target="_blank">
    <img src="https://img.shields.io/badge/Chat%20on-Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram">
  </a>&nbsp;
  <a href="https://wa.me/923249868488?text=Hi%20BitBash%2C%20I'm%20interested%20in%20automation." target="_blank">
    <img src="https://img.shields.io/badge/Chat-WhatsApp-25D366?style=for-the-badge&logo=whatsapp&logoColor=white" alt="WhatsApp">
  </a>&nbsp;
  <a href="mailto:sale@bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Email-sale@bitbash.dev-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Gmail">
  </a>&nbsp;
  <a href="https://bitbash.dev" target="_blank">
    <img src="https://img.shields.io/badge/Visit-Website-007BFF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Website">
  </a>
</p>




<p align="center" style="font-weight:600; margin-top:8px; margin-bottom:8px;">
  Created by Bitbash, built to showcase our approach to Scraping and Automation!<br>
  If you are looking for <strong>Yellowpages US Scraper and Extractor</strong> you've just found your team — Let’s Chat. 👆👆
</p>


## Introduction
This project automates the extraction of structured business data from Yellow Pages across the United States. It solves the challenge of manually gathering accurate business information and reduces the time needed for lead generation. Ideal for marketers, analysts, researchers, and businesses seeking clean, organized, and actionable data.

### Why This Scraper Is Effective
- Captures complete business profiles including contact info, ratings, reviews, and hours.
- Handles multiple keywords and locations in a single run.
- Delivers fast, optimized data collection with minimal resource usage.
- Supports sorting options to refine the business results.
- Ideal for building location-based targeted marketing campaigns.

## Features
| Feature | Description |
|---------|-------------|
| Multi-keyword scraping | Extract data for several industries or services simultaneously. |
| Location-based filtering | Target cities, states, or metro areas for hyper-local lead generation. |
| Comprehensive business fields | Collect names, phone numbers, emails, websites, hours, reviews, and more. |
| Sort & refine results | Sort businesses by relevance, distance, rating, or name. |
| High-speed performance | Optimized engine ensures fast, efficient extraction for large datasets. |
| Cost-efficient execution | Built to reduce resource usage while maintaining accuracy. |

---

## What Data This Scraper Extracts
| Field Name | Field Description |
|------------|------------------|
| name | Full business name. |
| address | Complete physical address including city, state, and ZIP. |
| phone | Primary business contact number. |
| email | Business email address if available. |
| website | Official website URL. |
| ratings | Ratings from Yellow Pages and external sources. |
| categories | Business categories or service types. |
| hours | Operating hours for each day. |
| gallery | URLs of gallery images. |
| ypReviews | List of reviews including reviewer, date, rating, and content. |
| generalInfo | General business description or overview. |

---

## Example Output

    {
      "name": "ZaSpa",
      "address": "2332 Something St Dallas, TX 75201",
      "phone": "(222) 222-2222",
      "email": "example@hotelzaza.com",
      "website": "https://www.hotelzaza.com/",
      "ratings": {
        "yellowpages": "8",
        "tripadvisor": "3"
      },
      "categories": ["Day Spas", "Beauty Salons", "Hair Removal"],
      "hours": [
        {
          "day": "Mon - Sat:",
          "time": "9:00 am - 8:00 pm"
        }
      ],
      "gallery": [
        "https://i2.ypcdn.com/blob/6e8975e0722b9001f7a8cfd5d8c70c48a45366d5_228x168_crop.jpg"
      ],
      "ypReviews": [
        {
          "reviewer": "staciesellers28",
          "reviewDate": "03/05/2013",
          "reviewRating": 0,
          "reviewContent": "Alexis, as always, was wonderful help when making my reservation."
        }
      ],
      "generalInfo": "ZaSpa Dallas is a day spa that features sitting areas and treatment rooms."
    }

---

## Directory Structure Tree

    Yellowpages US Scraper and Extractor/
    ├── src/
    │   ├── runner.py
    │   ├── extractors/
    │   │   ├── yp_parser.py
    │   │   └── utils_formatting.py
    │   ├── outputs/
    │   │   └── exporters.py
    │   └── config/
    │       └── settings.example.json
    ├── data/
    │   ├── inputs.sample.json
    │   └── sample_output.json
    ├── requirements.txt
    └── README.md

---

## Use Cases
- **Marketing agencies** use it to gather targeted business leads for outreach, improving campaign precision.
- **Sales teams** use it to create verified contact lists, helping them reduce bounce rates and improve conversions.
- **Researchers** extract structured business datasets for market studies and competitive analysis.
- **Entrepreneurs** use it to validate locations, industries, or market opportunities before launching new services.
- **Local service providers** build lists of potential partners or clients within their operating area.

---

## FAQs
**Q: Can this scraper handle multiple keywords and locations at once?**
Yes, it supports arrays of keywords and flexible location formatting, enabling large-scale data extraction.

**Q: What formats can I export the data to?**
Data can be exported in JSON or CSV formats for use in CRMs, spreadsheets, or data pipelines.

**Q: Does it capture images and reviews?**
Yes, it extracts gallery image URLs as well as detailed customer reviews when available.

**Q: Is sorting supported?**
You can sort results by best match, distance, rating, or alphabetical order.

---

## Performance Benchmarks and Results
- **Primary Metric:** Achieves fast extraction speeds, gathering hundreds of business records within minutes.
- **Reliability Metric:** Maintains a high success rate even during large multi-keyword runs.
- **Efficiency Metric:** Uses optimized resource handling to reduce memory and processing overhead.
- **Quality Metric:** Produces clean, structured, and complete business profiles ready for marketing and analytics workflows.


<p align="center">
<a href="https://calendar.app.google/74kEaAQ5LWbM8CQNA" target="_blank">
  <img src="https://img.shields.io/badge/Book%20a%20Call%20with%20Us-34A853?style=for-the-badge&logo=googlecalendar&logoColor=white" alt="Book a Call">
</a>
  <a href="https://www.youtube.com/@bitbash-demos/videos" target="_blank">
    <img src="https://img.shields.io/badge/🎥%20Watch%20demos%20-FF0000?style=for-the-badge&logo=youtube&logoColor=white" alt="Watch on YouTube">
  </a>
</p>
<table>
  <tr>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/MLkvGB8ZZIk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review1.gif" alt="Review 1" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash is a top-tier automation partner, innovative, reliable, and dedicated to delivering real results every time.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Nathan Pennington
        <br><span style="color:#888;">Marketer</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtu.be/8-tw8Omw9qk" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review2.gif" alt="Review 2" width="100%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Bitbash delivers outstanding quality, speed, and professionalism, truly a team you can rely on.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Eliza
        <br><span style="color:#888;">SEO Affiliate Expert</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
    <td align="center" width="33%" style="padding:10px;">
      <a href="https://youtube.com/shorts/6AwB5omXrIM" target="_blank">
        <img src="https://github.com/za2122/footer-section/blob/main/media/review3.gif" alt="Review 3" width="35%" style="border-radius:12px; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
      </a>
      <p style="font-size:14px; line-height:1.5; color:#444; margin:0 15px;">
        “Exceptional results, clear communication, and flawless delivery. Bitbash nailed it.”
      </p>
      <p style="margin:10px 0 0; font-weight:600;">Syed
        <br><span style="color:#888;">Digital Strategist</span>
        <br><span style="color:#f5a623;">★★★★★</span>
      </p>
    </td>
  </tr>
</table>
