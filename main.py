import scrape
import movie
import ides
import clear


scrape.fetch_posts("askreddit",field=10,num_of_comments=3,by_type="hot")



#scrape.screenshot_output()
scrape.take_screenshots(scrape.output["url"],scrape.output["id"])

scrape.voice_over_mp3()

primary = movie.make_output_clip(scrape.output["id"],scrape.output["comment_ides"])
primary.write_videofile("output/video.mp4", fps=24)

clear.clean.temp_clear()