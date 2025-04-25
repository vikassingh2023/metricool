import json
from typing import Any

import httpx

from ..config import METRICOOL_USER_TOKEN


async def make_get_request(url: str) -> dict[str, Any] | None:
    """Make a get request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def make_post_request(url: str, data: json) -> dict[str, Any] | None:
    """Make a post request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
        "content-type": "application/json",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, data=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def make_put_request(url: str, data: json) -> dict[str, Any] | None:
    """Make a put request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
        "content-type": "application/json",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(url, headers=headers, data=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

async def make_patch_request(url: str, data: json) -> int | None:
    """Make a patch request to the Metricool API with proper error handling."""
    headers = {
        "X-Mc-Auth": METRICOOL_USER_TOKEN,
        "content-type": "application/json",
        "accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(url, headers=headers, data=data, timeout=30.0)
            response.raise_for_status()
            return response.status_code
        except Exception:
            return None

DATA = {
    "providers": [
        {
            "network": "<string>",
            "id": "<string>",
            "status": "PUBLISHED",
            "publicUrl": "<string>",
            "detailedStatus": "<string>"
        },
        {
            "network": "<string>",
            "id": "<string>",
            "status": "ERROR",
            "publicUrl": "<string>",
            "detailedStatus": "<string>"
        }
    ],
    "publicationDate": {
        "dateTime": "<string>",
        "timezone": "<string>"
    },
    "text": "<string>",
    "id": "<integer>",
    "creationDate": {
        "dateTime": "<string>",
        "timezone": "<string>"
    },
    "firstCommentText": "<string>",
    "media": [
        "<string>",
        "<string>"
    ],
    "autoPublish": "<boolean>",
    "saveExternalMediaFiles": "<boolean>",
    "mediaAltText": [
        "<string>",
        "<string>"
    ],
    "shortener": "<boolean>",
    "draft": "<boolean>",
    "location": {
        "name": "<string>",
        "link": "<string>",
        "id": "<string>",
        "location": {
            "city": "<string>",
            "country": "<string>",
            "state": "<string>",
            "street": "<string>",
            "zip": "<string>",
            "latitude": "<double>",
            "longitude": "<double>"
        },
        "deleted": "<boolean>"
    },
    "videoCoverMilliseconds": "<long>",
    "videoThumbnailUrl": "<string>",
    "parentId": "<integer>",
    "twitterData": {
        "tags": [
            {
                "username": "<string>",
                "x": "<double>",
                "y": "<double>",
                "deleted": "<boolean>"
            },
            {
                "username": "<string>",
                "x": "<double>",
                "y": "<double>",
                "deleted": "<boolean>"
            }
        ]
    },
    "facebookData": {
        "boost": "<double>",
        "boostPayer": "<string>",
        "boostBeneficiary": "<string>",
        "type": "<string>",
        "title": "<string>"
    },
    "smartLinkData": {
        "targetUrl": "<string>",
        "ids": [
            "<integer>",
            "<integer>"
        ]
    },
    "instagramData": {
        "autoPublish": "<boolean>",
        "tags": [
            {
                "username": "<string>",
                "x": "<double>",
                "y": "<double>",
                "deleted": "<boolean>"
            },
            {
                "username": "<string>",
                "x": "<double>",
                "y": "<double>",
                "deleted": "<boolean>"
            }
        ],
        "productTags": [
            {
                "productName": "<string>",
                "productId": "<string>",
                "x": "<double>",
                "y": "<double>",
                "catalogId": "<string>"
            },
            {
                "productName": "<string>",
                "productId": "<string>",
                "x": "<double>",
                "y": "<double>",
                "catalogId": "<string>"
            }
        ],
        "carouselTags": {
            "enim1": [
                {
                    "username": "<string>",
                    "x": "<double>",
                    "y": "<double>",
                    "deleted": "<boolean>"
                },
                {
                    "username": "<string>",
                    "x": "<double>",
                    "y": "<double>",
                    "deleted": "<boolean>"
                }
            ]
        },
        "carouselProductTags": {
            "pariatur3": [
                {
                    "productName": "<string>",
                    "productId": "<string>",
                    "x": "<double>",
                    "y": "<double>",
                    "catalogId": "<string>"
                },
                {
                    "productName": "<string>",
                    "productId": "<string>",
                    "x": "<double>",
                    "y": "<double>",
                    "catalogId": "<string>"
                }
            ],
            "pariatur__": [
                {
                    "productName": "<string>",
                    "productId": "<string>",
                    "x": "<double>",
                    "y": "<double>",
                    "catalogId": "<string>"
                },
                {
                    "productName": "<string>",
                    "productId": "<string>",
                    "x": "<double>",
                    "y": "<double>",
                    "catalogId": "<string>"
                }
            ]
        },
        "type": "<string>",
        "showReelOnFeed": "<boolean>",
        "boost": "<double>",
        "boostPayer": "<string>",
        "boostBeneficiary": "<string>",
        "audioName": "<string>",
        "collaborators": [
            {
                "username": "<string>",
                "deleted": "<boolean>"
            },
            {
                "username": "<string>",
                "deleted": "<boolean>"
            }
        ]
    },
    "pinterestData": {
        "boardId": "<string>",
        "pinTitle": "<string>",
        "pinLink": "<string>",
        "pinNewFormat": "<boolean>"
    },
    "youtubeData": {
        "title": "<string>",
        "type": "<string>",
        "privacy": "<string>",
        "tags": [
            "<string>",
            "<string>"
        ],
        "category": "<string>",
        "madeForKids": "<boolean>"
    },
    "tiktokData": {
        "disableComment": "<boolean>",
        "disableDuet": "<boolean>",
        "disableStitch": "<boolean>",
        "privacyOption": "<string>",
        "commercialContentThirdParty": "<boolean>",
        "commercialContentOwnBrand": "<boolean>",
        "title": "<string>",
        "autoAddMusic": "<boolean>",
        "photoCoverIndex": "<integer>"
    },
    "linkedinData": {
        "documentTitle": "<string>",
        "publishImagesAsPDF": "<boolean>",
        "previewIncluded": "<boolean>",
        "type": "<string>",
        "poll": {
            "question": "<string>",
            "options": [
                {
                    "text": "<string>"
                },
                {
                    "text": "<string>"
                }
            ],
            "settings": {
                "duration": "<string>"
            }
        }
    },
    "autolistData": {
        "id": "<integer>",
        "name": "<string>"
    },
    "brandName": "<string>",
    "targetBrandId": "<integer>",
    "gmbData": {
        "type": "<string>"
    },
    "descendants": [
        {
            "value": "<Circular reference to #/components/schemas/ScheduledPost detected>"
        },
        {
            "value": "<Circular reference to #/components/schemas/ScheduledPost detected>"
        }
    ],
    "notes": [
        {
            "created": {
                "dateTime": "<string>",
                "timezone": "<string>"
            },
            "id": "<integer>",
            "postId": "<integer>",
            "userId": "<integer>",
            "userName": "<string>",
            "content": "<string>",
            "updatedDate": {
                "dateTime": "<string>",
                "timezone": "<string>"
            },
            "updated": "<boolean>",
            "deletedDate": {
                "dateTime": "<string>",
                "timezone": "<string>"
            },
            "deleted": "<boolean>"
        },
        {
            "created": {
                "dateTime": "<string>",
                "timezone": "<string>"
            },
            "id": "<integer>",
            "postId": "<integer>",
            "userId": "<integer>",
            "userName": "<string>",
            "content": "<string>",
            "updatedDate": {
                "dateTime": "<string>",
                "timezone": "<string>"
            },
            "updated": "<boolean>",
            "deletedDate": {
                "dateTime": "<string>",
                "timezone": "<string>"
            },
            "deleted": "<boolean>"
        }
    ],
    "hasNotReadNotes": "<boolean>",
    "uuid": "<string>",
    "copiedFrom": "<string>",
    "creatorUserMail": "<string>",
    "creatorUserId": "<integer>",
    "postApprovalData": {
        "approvalEvents": [
            {
                "postUuid": "<string>",
                "postId": "<integer>",
                "reviewerId": "<integer>",
                "reviewerMail": "<string>",
                "status": "<string>",
                "updatedDate": {
                    "dateTime": "<string>",
                    "timezone": "<string>"
                },
                "deletedDate": {
                    "dateTime": "<string>",
                    "timezone": "<string>"
                },
                "deleted": "<boolean>"
            },
            {
                "postUuid": "<string>",
                "postId": "<integer>",
                "reviewerId": "<integer>",
                "reviewerMail": "<string>",
                "status": "<string>",
                "updatedDate": {
                    "dateTime": "<string>",
                    "timezone": "<string>"
                },
                "deletedDate": {
                    "dateTime": "<string>",
                    "timezone": "<string>"
                },
                "deleted": "<boolean>"
            }
        ],
        "approvalStatus": "<string>",
        "approvalCriteria": "<string>",
        "sendMailToReviewers": "<boolean>",
        "saveData": "<boolean>"
    },
    "threadsData": {
        "allowedCountryCodes": [
            "<string>",
            "<string>"
        ]
    },
    "blueskyData": {
        "postLanguages": [
            "<string>",
            "<string>"
        ]
    },
    "libraryPostId": "<long>"
}