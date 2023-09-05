import dotenv
import argparse
import os
import json

from yts.qa import YoutubeQA
from yts.summarize import YoutubeSummarize

DEFAULT_VIDEO_ID = "cEynsEWpXdA" #"Tia4YJkNlQ0" # 西園寺
DEFAULT_REF_SOURCE = 3

dotenv.load_dotenv()


def qa (args):
    yqa = YoutubeQA(args.vid, args.source, args.detail, args.debug)
    yqa.prepare_query()

    # ちょっとサービス（要約があれば表示する）
    if os.path.exists(f'{os.environ["SUMMARY_STORE_DIR"]}/{args.vid}'):
        with open(f'{os.environ["SUMMARY_STORE_DIR"]}/{args.vid}', 'r') as f:
            summary = json.load(f)
        print(f'(Summary) {summary["concise"]}\n')

    while True:
        query = input("Query: ").strip()
        if query == "":
            break
        print('Answer: ', end="", flush=True)
        answer = yqa.run_query(query)
        print(f'{answer}\n')

        if args.detail:
            for score, id, time, source in yqa.get_source():
                print(f"--- {time} ({id} [{score}]) ---\n {source}")
            print("")


def summary (args):
    ys = YoutubeSummarize(args.vid, args.debug)
    ys.prepare()
    summary = ys.run()

    print('[詳細な要約]')
    for s in summary["detail"]:
        print(f'・{s}\n')
    print("\n", "[簡潔な要約]\n", summary["concise"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Youtube動画の視聴を支援するスクリプト')
    parser.add_argument('--vid', default=DEFAULT_VIDEO_ID, help=f'Youtube動画のID（default:{DEFAULT_VIDEO_ID}）')
    parser.add_argument('--source', default=DEFAULT_REF_SOURCE, type=int, help=f'回答を生成する際に参照する検索結果の数を指定する（default:{DEFAULT_REF_SOURCE}）')
    parser.add_argument('--detail', action='store_true', help='回答生成する際に参照した検索結果を表示する')
    parser.add_argument('--debug', action='store_true', help='デバッグ情報を出力する')
    parser.add_argument('--summary', action='store_true', help='要約する')
    args = parser.parse_args()

    if args.summary is False:
        qa(args)

    if args.summary is True:
        summary(args)