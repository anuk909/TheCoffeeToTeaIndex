import unittest
from unittest.mock import patch, MagicMock
import logging
from extract_subtitles import extract_subtitles
from youtube_transcript_api import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable, CouldNotRetrieveTranscript

class TestExtractSubtitles(unittest.TestCase):

    @patch('extract_subtitles.YouTubeTranscriptApi.get_transcript')
    def test_successful_subtitle_extraction(self, mock_get_transcript):
        mock_get_transcript.return_value = [{'text': 'Hello world'}, {'text': 'This is a test'}]
        video_id = 'dQw4w9WgXcQ'
        subtitles = extract_subtitles(video_id)
        self.assertEqual(subtitles, ['Hello world', 'This is a test'])

    @patch('extract_subtitles.YouTubeTranscriptApi.get_transcript')
    def test_invalid_video_id_format(self, mock_get_transcript):
        video_id = 'invalid_id'
        with self.assertLogs(level='ERROR') as log:
            subtitles = extract_subtitles(video_id)
            self.assertIn('Invalid video_id format', log.output[0])
        self.assertEqual(subtitles, [])

    @patch('extract_subtitles.YouTubeTranscriptApi.get_transcript')
    def test_transcripts_disabled(self, mock_get_transcript):
        mock_get_transcript.side_effect = CouldNotRetrieveTranscript('video_id', 'requested_language_codes', 'transcript_data')
        video_id = 'dQw4w9WgXcQ'
        with self.assertLogs(level='ERROR') as log:
            subtitles = extract_subtitles(video_id)
            self.assertIn('Could not retrieve transcript for video_id', log.output[0])
        self.assertEqual(subtitles, [])

    @patch('extract_subtitles.YouTubeTranscriptApi.get_transcript')
    def test_no_transcript_found(self, mock_get_transcript):
        mock_get_transcript.side_effect = CouldNotRetrieveTranscript('video_id', 'requested_language_codes', 'transcript_data')
        video_id = 'dQw4w9WgXcQ'
        with self.assertLogs(level='ERROR') as log:
            subtitles = extract_subtitles(video_id)
            self.assertIn('Could not retrieve transcript for video_id', log.output[0])
        self.assertEqual(subtitles, [])

    @patch('extract_subtitles.YouTubeTranscriptApi.get_transcript')
    def test_video_unavailable(self, mock_get_transcript):
        mock_get_transcript.side_effect = CouldNotRetrieveTranscript('video_id', 'requested_language_codes', 'transcript_data')
        video_id = 'dQw4w9WgXcQ'
        with self.assertLogs(level='ERROR') as log:
            subtitles = extract_subtitles(video_id)
            self.assertIn('Could not retrieve transcript for video_id', log.output[0])
        self.assertEqual(subtitles, [])

    @patch('extract_subtitles.YouTubeTranscriptApi.get_transcript')
    def test_unexpected_error(self, mock_get_transcript):
        mock_get_transcript.side_effect = Exception('Unexpected error')
        video_id = 'dQw4w9WgXcQ'
        with self.assertLogs(level='ERROR') as log:
            subtitles = extract_subtitles(video_id)
            self.assertIn('An unexpected error occurred while extracting subtitles', log.output[0])
        self.assertEqual(subtitles, [])

if __name__ == '__main__':
    unittest.main()
