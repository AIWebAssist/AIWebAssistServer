from abc import ABC, abstractmethod
from scrape_anything.act.tool import ToolInterface
from ..view import *
from ..util import dataframe_to_csv,bytes_to_file,elements_to_table
import os


class Controller(ABC):

    def __init__(self,user_task:str) -> None:
        self.user_task = user_task

    @abstractmethod
    def fetch_infomration_on_screen(self,output_folder:str,loop_num:int):
        pass

    @abstractmethod
    def on_action_extraction_failed(self,loop_num:int):
        pass

    @abstractmethod
    def on_action_extraction_fatal(self,loop_num:int):
        pass

    def process_screen_data(self,incoming_data,output_folder,loop_num,file_name_html=None):

        raw_on_screen, viewpointscroll,viewportHeight,scroll_width,scroll_height = elements_to_table(incoming_data.raw_on_screen),incoming_data.viewpointscroll,incoming_data.viewportHeight,incoming_data.scroll_width,incoming_data.scroll_height
        width = incoming_data.width
        height = incoming_data.height
        url = incoming_data.url
        screenshot_path = bytes_to_file(incoming_data.screenshot,os.path.join(output_folder,f"step_{loop_num+1}_screenshot.png"))

        scroll_ratio = f"On the Width Axis, {scroll_width}. On the Height Axis, {scroll_height}"
        screen_size = f"width={width},height={height}"
        # store the raw elements before processing
        dataframe_to_csv(raw_on_screen,f"{output_folder}/step_{loop_num+1}_raw.csv") 


        # minimize the data sent to the llm + enrich
        on_screen = minimize_and_enrich_page_data(raw_on_screen,viewpointscroll,viewportHeight,screenshot_path)
        # store the minimized elements
        dataframe_to_csv(on_screen,f"{output_folder}/step_{loop_num+1}_minimized.csv") 
        
        
        return on_screen,viewpointscroll,viewportHeight,screen_size,screenshot_path,file_name_html,scroll_ratio,url,self.user_task

        
    @abstractmethod
    def take_action(self,tool_executor:ToolInterface, tool_input:str,num_loops:int,output_folder:str):
        pass

    @abstractmethod
    def is_closed(self):
        pass
    
    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def from_pickle(self, output_folder, loop_num):
        pass